# Batch Processing

## Index
1. [Apache Spark](#apache-spark)
    - [Environment Setup](#env-setup)
    - [Spark Cluster](#spark-cluster)
    - [Repartition](#spark-repartition)
    - [Spark & GCS] (#spark-gcs)
2. [Download Green & Yello data](#dowload-data)


----

Different ways for processing data:

- **BATCH:** Processes big chuncks of data in one go, according to a certain granularity (ie. weekly, hourly, 3 times per hours, etc)
    -- ***Technologies:*** Python scripts, SQL, Spark, Flink, etc.
    -- ***Advantages:*** Easier to scale, manage and retry (when there are errors)
    -- ***Disadvantage:*** Delay of processing, the data is not immediately available


- **STREAMING**



----



<a id="apache-spark"></a>
## 1. Apache Spark

Data processing engine, which can use different languages

<img src="../images/apache-spark.png" width="80%">


**When to use Spark?** You have data in a datalake, Spark will pull this data, do some processing, and send the data back to the datalake. When your transformations are too complex that you cannot express them with SQL, you can use Spark. 

<a id="env-setup"></a>

### 1.1 Environment Setup

**[Environment Setup](01_env_setup.md)** (MacOS Sequoia, brew + anaconda)

-------
<a id="spark-cluster"></a>

### 1.2 Spark Cluster
A **Spark cluster** is a group of computers (or nodes) working together to process **large datasets** using Apache Spark. It allows you to split complex tasks across multiple machines, making data processing **faster** and **scalable**.

**🧱 Basic Structure of a Spark Cluster**
A Spark cluster has three main components:

1. **Driver Node** (Master)  
- **Brain of the cluster** – coordinates tasks, tracks progress, and combines results.  
- It sends tasks to worker nodes and collects the output.

2. **Worker Nodes** (Executors)  
- **Muscle of the cluster** – perform the actual data processing.  
- Each worker gets a portion of the data and runs tasks in **parallel**.  

3. **Cluster Manager**  
- **Traffic controller** – manages resources (CPU, memory) and assigns tasks to workers.  
- Examples: **YARN**, **Kubernetes**, **Standalone** (built-in Spark manager).  


**How Does It Work?**
1. **You Submit a Job** (e.g., run a Spark script).
2. **Driver Node** splits the job into smaller tasks.
3. **Cluster Manager** assigns these tasks to **Worker Nodes**.
4. **Worker Nodes** process the data in parallel.
5. **Driver Node** collects and combines the results.


---


<a id="spark-repartition"></a>

### 1.3 Understanding `.repartition()` in Apache Spark

The `.repartition()` method in **Apache Spark** is used to **increase or decrease the number of partitions** in a DataFrame or RDD. Partitions represent chunks of data that Spark processes in parallel.



**🔍 Key Purposes of `.repartition()`**

1. **Optimize Performance**  
   - **Increase partitions** to **speed up** large dataset processing by enabling more parallel execution.  
   - **Decrease partitions** to **reduce overhead** when working with small datasets and prevent excessive task creation.

2. **Balance Data Distribution**  
   - Helps prevent **data skew** by ensuring that the workload is evenly spread across cluster nodes.

3. **Improve Resource Utilization**  
   - Ensures efficient use of **CPU and memory** by distributing data evenly across Spark executors.

---

**📊 Example Usage**

```python
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder.appName("RepartitionExample").getOrCreate()

# Sample DataFrame
data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
df = spark.createDataFrame(data, ["Name", "Age"])

# Check current partitions
print(df.rdd.getNumPartitions())  # Example: 1 partition by default in local mode

# Increase to 4 partitions
df_repartitioned = df.repartition(4)

print(df_repartitioned.rdd.getNumPartitions())  # Output: 4
```

---

**📌 `.repartition()` vs `.coalesce()`**

| Feature          | `.repartition()`                     | `.coalesce()`                  |
|------------------|-------------------------------------|--------------------------------|
| **Usage**        | Increase **or** decrease partitions  | **Decrease** partitions only   |
| **Shuffle**      | **Yes** (Full data shuffle)          | **No** (Minimizes data movement) |
| **Performance**  | Slower due to **shuffling**          | Faster—**no full shuffle**     |
| **When to use?** | **Balance** large data across cluster| Optimize **small** datasets or **merge** partitions |


**✅ Best Practices**

- Use **`.repartition()`** when you need **even distribution** or to **increase** partitions.
- Use **`.coalesce()`** to **reduce** partitions with **minimal shuffling** (faster).
- Avoid **too many** partitions (overhead) or **too few** (bottlenecks).
- Aim for **128 MB – 256 MB** of data per partition for **optimal performance**.

---

<a id="spark-gcs"></a>

### 1.4 Spark & Google Cloud
All the files are [here](./06_spark_gcs.ipynb)

----

<a id="download-data"></a>

## 2. Download Green & Yellow data 🚖

- We will use [this script](download_data.sh). 

- First you need to make script executable:
`chmod +x download_data.sh`

- The run the script, also adding the parameters for Green/yellow and year:
`download_data.sh green 2020`

- Follow the [03_taxi_schema](03_taxi_schema.ipynb)

- You can see the jobs at `localhost:4040``
<img src="./img/spark_job_example.png" width="80%">

---








