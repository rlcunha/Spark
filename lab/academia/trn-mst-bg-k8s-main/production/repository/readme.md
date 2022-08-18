```sh
# connect into prod cluster
kubectx aks-owshq-prod 

# create namespace
k create namespace ingestion

# install helm repo
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# install strimzi operator
helm install kafka strimzi/strimzi-kafka-operator --namespace ingestion --version 0.26.0

# install kafka cluster with ephemeral option
k apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/production/repository/broker/kafka-ephemeral.yaml -n ingestion

# retrieve info from kubernetes
# https://strimzi.io/docs/operators/latest/overview.html
# https://strimzi.io/docs/operators/latest/using.html

# retrieve nodes info
k get nodes --show-labels
k get nodes
k get nodes -l agentpool=agentpool
k describe node -l agentpool=agentpool

k get nodes -l agentpool=npd8sv3
k describe nodes -l agentpool=npd8sv3

k get nodes -l agentpool=npds3v2
k describe nodes -l agentpool=npd8sv3

# get kafka info
kubens ingestion
kgp -o wide

#-----------------------------------#
#-----------------------------------#
# make kafka cluster production-ready
#-----------------------------------#
#-----------------------------------#

# https://www.youtube.com/watch?v=u1n9rg7pELo
# 1) taint the select worker nodes
# 2) add labels to tainted nodes
# 3) drain all other applications
# 4) configure tolerations in kafka
# 5) configure node-affinity in kafka
 
# retrieve node pool to host strimzi
k get nodes -l agentpool=npd8sv3
aks-npd8sv3-22409415-vmss000000
aks-npd8sv3-22409415-vmss000001
aks-npd8sv3-22409415-vmss000002

# taint nodes to not receive different apps 
k taint node aks-npd8sv3-22409415-vmss000000 dedicated=Kafka:NoSchedule --overwrite 
k taint node aks-npd8sv3-22409415-vmss000001 dedicated=Kafka:NoSchedule --overwrite 
k taint node aks-npd8sv3-22409415-vmss000002 dedicated=Kafka:NoSchedule --overwrite 

# get taint info
k describe nodes -l agentpool=npd8sv3
  
# create a label 
k label node aks-npd8sv3-22409415-vmss000000 dedicated=Kafka --overwrite 
k label node aks-npd8sv3-22409415-vmss000001 dedicated=Kafka --overwrite 
k label node aks-npd8sv3-22409415-vmss000002 dedicated=Kafka --overwrite 

# describe nodes
k describe nodes -l agentpool=npd8sv3

# configure tolerations and node affinity
# strimzi deployment spec - apply changes
k apply -f /Users/luanmorenomaciel/BitBucket/big-data-on-k8s/production/repository/broker/kafka-ephemeral.yaml -n ingestion

# dedicated strimzi deployment (isolation)
/*
template:
  pod:
    tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "kafka-strimzi-operator"
        effect: "NoSchedule"
    affinity:
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
            - matchExpressions:
                - key: dedicated
                  operator: In
                  values:
                    - kafka-strimzi-operator
*/

# pod affinity and anti-affinity
# never scheduled on same node
# database, storage, messaging system

/*
pod:
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
            - key: workload
              operator: In
              values:
                - rdbms
                - nosql
        topologyKey: "kubernetes.io/hostname"
nodeAffinity:
requiredDuringSchedulingIgnoredDuringExecution:
  nodeSelectorTerms:
    - matchExpressions:
        - key: type
          operator: In
          values:
          - npds3v2
*/

# rack awareness
k describe nodes -l agentpool=npd8sv3

k describe node --selector agentpool=npd8sv3,topology.kubernetes.io/zone=eastus2-1
k describe node --selector agentpool=npd8sv3,topology.kubernetes.io/zone=eastus2-2
k describe node --selector agentpool=npd8sv3,topology.kubernetes.io/zone=eastus2-3

# housekeeping
k delete kafka.kafka.strimzi.io/edh
helm delete kafka -n ingestion
```