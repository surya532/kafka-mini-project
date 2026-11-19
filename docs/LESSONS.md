# Lessons learned

Notes from running the experiments in this repo locally with Docker and `kafka-python`.

## 1. Keys decide ordering

I ran the producer with `user_id` as the key, then again with no key, and watched the partition numbers on the consumer side.

With the key set, every event for the same user landed on the same partition, in the order it was sent. Without a key, the same user's events were spread across partitions. Kafka only guarantees order inside a single partition, so once events for one user are on different partitions, nothing keeps them in sequence when they're consumed.

The takeaway for me: if order matters for an entity, the key has to be that entity's id.

## 2. Rebalancing is not instant

I started two consumers in one group and stopped one of them. Stopping with `Ctrl+C` let the consumer leave the group cleanly, and the other consumer picked up its partitions after about ___ seconds. When I killed one with `kill -9`, the group had to wait for the session timeout before it noticed, and the partitions sat idle for about 5 seconds.

That gap is the part that surprised me. During a rebalance, the affected partitions aren't being processed at all, so a consumer crashing is a pause in processing and not only a lost worker.

## 3. A new group_id replays everything

Offsets are stored per consumer group, not per topic. When I changed `group_id`, the new group had no saved position, so it started from the beginning because I'd set `auto_offset_reset="earliest"`. The data was still on the broker the whole time. Kafka keeps messages according to its retention settings, and consuming them doesn't remove them.

This is what makes replay and backfill possible, and it's the first big difference from a queue.

## 4. Groups are what split the work

Two consumers in the same group divided the three partitions between them, so each message was handled once. Two consumers in different groups each received every message. If I wanted workers to share a load but put them in different groups by mistake, they'd all do all the work, and any side effect would happen more than once.

## 5. Why not just use a queue

With a queue like SQS, a message is deleted once it's processed. Kafka keeps the log, so I could re-read old events, run independent consumers on the same data, and reason about order per partition. This project is about those streaming properties, not about task distribution.

## What this project doesn't cover

Kafka delivers messages at least once. After a crash or a rebalance, a consumer can see the same message again, and this project does nothing about duplicates. My Java project, [`idempotent-kafka-pipeline`](https://github.com/surya532/idempotent-kafka-pipeline), handles that with idempotent processing, retries, and a dead-letter topic.
