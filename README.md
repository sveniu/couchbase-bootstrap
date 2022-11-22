# Bootstrap a Couchbase cluster

Before running this program, the expected state is:

* Couchbase Server is installed and running

* The cluster has not been initialized

* The node itself has not been initialized

After running, the state is:

* The cluster is initialized with credentials

* Member nodes have joined the cluster

* Settings have been applied: memory quotas, indexer settings, autofailover
  settings, etc.

* Buckets have been created

* Users have been created

* CBQ scripts have been executed

Caveats:

* Nodes join the cluster, but no rebalance takes place.

* CBQ scripts can't create indexes with num_replica greater than 0, because
  there are no actively joined nodes in the cluster; a rebalance must happen
  first.
