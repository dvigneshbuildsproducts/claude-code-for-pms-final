# How Rook works: Dispatch, handlers and responders

Sources: rook-wiki (About Rook, Glossary, Rook Dispatch, Rook Supply) and
`00-rook/code/dispatch-routing/`. The diagrams render on GitHub.

## 1. Who's who

```mermaid
flowchart LR
    ROOK["Rook Industries<br/>sells software,<br/>priced per active responder"]

    subgraph Customers["Customers (not Rook employees)"]
        H["Handler<br/>looks after one or a few responders"]
        R["Responder<br/>takes callouts, goes to incidents"]
        Q["Quartermaster<br/>owns gear stock and approvals"]
    end

    subgraph Products["Rook products"]
        D["Rook Dispatch<br/>who gets pinged about a callout"]
        S["Rook Supply<br/>gear: requisitions, maintenance, failures"]
    end

    ROOK --> D
    ROOK --> S
    H -- "web console" --> D
    R -- "phone app" --> D
    H -- "requisitions, failure reports" --> S
    Q -- "approves, fulfils" --> S
    D -- "Responder Availability Record<br/>(Supply reads, never writes)" --> S
    H -- "support tickets" --> SUP["Rook Support<br/>callout tickets skip the queue"]
```

## 2. A callout, start to finish

```mermaid
flowchart TD
    A["Incident comes in<br/>(handler enters it, or an intake system pushes it)"] --> B["Dispatch lists every available responder"]
    B --> C["Rank them by routing priority:<br/>proximity (travel time) 0.60<br/>recent acceptance 0.25<br/>capability match 0.15"]
    C --> D["Ping the top responder's phone"]
    D --> E{"Answer within<br/>60 seconds?"}
    E -- "Taken" --> F["Responder engaged,<br/>incident assigned<br/>score +0.08"]
    E -- "Turned down" --> G["score −0.12"]
    E -- "No answer: missed" --> G
    G --> H{"Anyone left<br/>on the list?"}
    H -- "Yes" --> D2["Ping the next responder"] --> E
    H -- "No" --> I["Nobody took it"]
    O["Handler can override<br/>and pick someone else<br/>(logged since 4.0)"] -.-> D
```

## 3. Who sees what during a callout

```mermaid
sequenceDiagram
    participant H as Handler (console)
    participant D as Rook Dispatch
    participant R as Responder (phone)
    H->>D: Enter incident / set availability and tags
    D->>D: Rank available responders
    D->>R: Ping ("this one's yours?")
    Note over R: 60s to answer (90s before 4.2)
    alt Taken
        R->>D: Yes
        D->>H: Coverage view shows responder engaged
    else Turned down or missed
        R-->>D: No, or no answer
        D->>D: Lower score, ping next responder
    end
    Note over H: The handler is not alerted when their<br/>responder is pinged (asked for in interviews)
```

## 4. The scoring loop behind the 4.2 problem

```mermaid
flowchart LR
    M["Misses a ping<br/>(60s too short)"] --> P["Score −0.12<br/>(same as a 'no')"]
    P --> L["Ranks lower than<br/>nearby responders"]
    L --> F["Pinged rarely:<br/>only when others say no"]
    F --> X["Phone quiet for days,<br/>so the next ping is missed too"]
    X --> M
    N["No reset over time<br/>(2019 TODO in history.py)"] -.-> L
```
