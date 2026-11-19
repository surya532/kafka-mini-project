# One-time GitHub setup (2 minutes)

Using the GitHub CLI (`gh auth login` first):

```bash
gh repo edit surya532/kafka-mini-project \
  --description "Hands-on Kafka fundamentals: partitions, keys, consumer groups, offsets, replay, rebalancing (Python + Docker)" \
  --add-topic kafka --add-topic event-streaming --add-topic event-driven --add-topic python --add-topic docker
```

Or in the web UI: repo page → gear icon next to "About" → add description and topics.
