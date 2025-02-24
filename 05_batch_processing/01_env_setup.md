# Installing Spark on MacOS (with Anaconda environment + brew)

🖥️ MacOS Sequoia 15.3 (Intel), using Anaconda + brew

👩🏽‍💻 *Ps: The instructions from the course for setting up the env didn't work for me. Here's what worked for me:*

#### ✅ **Step 01: Install Java via brew. Note: It needs to be version 9 or 11.**

`brew install openjdk@11`

Next, considering I have my anaconda environment activated, I also installed `pyspark` and `findspark` via pip at this stage.


#### ✅ **Step 02: Use Full Path for JAVA_HOME**
Try setting JAVA_HOME using the full path to the JDK inside Homebrew’s installation:

`export JAVA_HOME=$(/usr/libexec/java_home -v 11 2>/dev/null || echo "/usr/local/opt/openjdk@11")`

Then check if it worked:

`java -version`

If that works, make it permanent:

```sh
echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 11 2>/dev/null || echo "/usr/local/opt/openjdk@11")' >> ~/.zshrc
source ~/.zshrc
```

#### ✅ **Alternative Step 02: Link Java to System Java Path**
Sometimes, macOS doesn’t detect Homebrew Java properly. Try linking it manually:

```sh
sudo ln -sfn /usr/local/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk
```

Then verify again:

```sh
java -version
```

#### ✅ **Step 03: Test in a notebook**

Also on file[testing_spark](testing_spark.ipynb)

```php
import pyspark
from pyspark.sql import SparkSession

!spark-shell --version

# Create SparkSession
spark = SparkSession.builder.master("local[1]") \
                    .appName('test-spark') \
                    .getOrCreate()

print(f'The PySpark {spark.version} version is running...')

```


#### ✅ **Step 04: Install Apache Spark**
Since `brew info apache-spark` says "Not installed," install it using:

```sh
brew install apache-spark
```

After the installation, find the path where its installed:

```sh
brew info apache-spark
```

It should return something like:
`/usr/local/Cellar/apache-spark/3.5.4`

Now add the required varuables to your ˜/.zshrc file:
```sh
echo 'export SPARK_HOME=/usr/local/Cellar/apache-spark/3.5.4/libexec' >> ~/.zshrc
echo 'export PATH="$SPARK_HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Note**: If your `brew --prefix apache-spark` command returned a different path,
replace `/usr/local/Cellar/apache-spark/3.5.4` with your actual path.


Verify the installation:
```sh
spark-shell --version
```

If everything is great, you should see something like this:

```swift
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.5.4
      /_/

````

#### ✅ **Step 05: Testing Spark**
Execute `spark-shell` and rung the following in scala:
```scala
val data = 1 to 10000
val distData = sc.parallelize(data)
distData.filter(_ < 10).collect()
```

You will see something like this:

```scala
scala> val data = 1 to 10000
data: scala.collection.immutable.Range.Inclusive = Range 1 to 10000

scala> val distData = sc.parallelize(data)
distData: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:24

scala> distData.filter(_ < 10).collect()
res0: Array[Int] = Array(1, 2, 3, 4, 5, 6, 7, 8, 9)
```
#### ✅ **Step 06: Testing PySpark**
Via shell, get the file we will be using:

`wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv`

Now, in a [notebook](testing_pyspark.ipynb), run the following:
```php
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

df = spark.read \
    .option("header", "true") \
    .csv('taxi_zone_lookup.csv')

df.show()
```

Test that writing also works:

````
df.write.parquet('zones')
````