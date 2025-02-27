# Streaming Processing

📝 [Notes nu ziritrion](https://github.com/ziritrion/dataeng-zoomcamp/blob/main/notes/6_streaming.md)
🦦 [Gentle down the stream - Illustrated introduction to Kakfa](https://www.gentlydownthe.stream/)

## Introduction to Apache Kafka

Apache Kafka is a **distributed event streaming platform** used to handle large amounts of real-time data. It’s like a message broker but designed to handle high throughput and scale easily.

<img src="./imgs/apache-kafta.png" width="70%">


### Why Use Kafka?
- **Real-time data:** Ideal for handling live event streams (e.g., website clicks, payments, or logs).
- **Scalability:** Handles huge data loads by spreading it across multiple servers.
- **Fault Tolerance:** If one broker fails, others take over, ensuring data isn’t lost.

### How Kafka Works:
- **Producers:** Send (or "produce") messages to Kafka. Example: A ride-sharing app sends trip data in real time.

- **Topics:** Messages are grouped by categories called topics—like folders where messages of the same type are stored.

- **Brokers:** Kafka servers that store and manage messages. You can have multiple brokers working together.

- **Clusters**: A collection of brokers that work togethers.

- **Consumers:** Read (or "consume") messages from Kafka. Example: Analytics systems that process the trip data.

- **Partitions:** Each topic is divided into partitions to enable parallel processing and increase performance.

**✅ How It All Comes Together**
1. Producer: A ride-sharing app sends a trip record (a letter) to Kafka.
2. Broker: Kafka receives it and stores it in a topic (a mail category).
3. Partition: The message is split across different partitions (shelves) for faster access.
4. Consumer: An analytics system reads the trip record and calculates the fare (a mail recipient).
5. ZooKeeper: Ensures all brokers are healthy and keeps track of who’s handling what (the postmaster).

#### Analogy: Kafka & Postoffices

**📤 Producers (Senders)**
These are the people sending letters (data) to the post office.
In Kafka, producers are applications that generate and send messages. For example:

- A ride-sharing app sends trip data when a ride starts.
- An e-commerce platform sends purchase information after every sale.

*👉 Analogy: Producers = People mailing letters.*



**📦 Topics (Mail Categories)**
Just like a post office sorts mail by categories (e.g., "Letters," "Packages," "Priority"), Kafka organizes messages by topics.
Each message belongs to a specific topic—you can think of it as a labeled mailbox.

- "trip_data" for ride information.
- "user_activity" for app interactions.

*👉 Analogy: Topics = Different mail categories.*



**📚 Partitions (Mail Sorting Shelves)**
To handle large volumes of mail efficiently, the post office doesn’t put all letters in a single box. Instead, it splits them across many shelves.

In Kafka, topics are divided into partitions to distribute the load. This allows Kafka to handle many messages in parallel, improving performance.Each message within a partition gets a unique order but partitions themselves process independently.

- A partition is assigned to ONLY one consumer; a consumer can have multiple partitions assigned to it.

*👉 Analogy: Partitions = Different shelves for each mail category.*

**📮 Brokers (Post Offices)**
A post office is where mail is received, stored, and dispatched. Kafka brokers work the same way.
Each Kafka broker stores a portion of the data (partitions) and handles requests from both producers and consumers.
If there’s a large city, it might have multiple post offices to distribute the work—similarly, Kafka uses many brokers to scale across systems.

👉 Analogy: Brokers = Post office branches managing the mail flow.

**📬 Consumers (Recipients)**
These are the people receiving letters from the post office.
In Kafka, consumers are the applications that read and process messages from topics.

For example:

- A data analytics tool reads trip data to track revenue.
- A monitoring system checks for errors in real-time logs.

*👉 Analogy: Consumers = People receiving and reading mail.*

**🔄 Consumer Groups (Delivery Routes)**
A city might have multiple mail carriers delivering letters on separate routes. This is like Kafka’s consumer groups—they share the workload of processing messages.
If a topic has 10 partitions and 5 consumers, each consumer gets a portion of the messages.

*👉 Analogy: Consumer groups = Different mail carriers delivering mail to specific neighborhoods.*

**📊 ZooKeeper (Postmaster)**
In a post office, the postmaster keeps track of all branches and ensures everything runs smoothly.
Kafka uses ZooKeeper to:

Track which brokers are active.
Manage leader elections (who’s in charge of each partition).
Maintain system health.

*👉 Analogy: ZooKeeper = The postmaster managing the entire post office network.*