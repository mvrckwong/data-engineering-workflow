```mermaid
graph LR
  Bronze -->|raw data| Silver
  Silver -->|cleansed data| Gold
  Gold -->|dimensions| Gold[Fact Table]
```