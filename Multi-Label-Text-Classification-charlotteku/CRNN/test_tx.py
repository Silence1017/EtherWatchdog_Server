# -*- coding:utf-8 -*-
__author__ = 'Randolph'
import requests
requests.adapters.DEFAULT_RETRIES =100
import os
import sys
import time
import logging
import pymongo
import json
import random
import numpy as np
from matplotlib import pyplot as plt

sys.path.append('../')
logging.getLogger('tensorflow').disabled = True

import tensorflow as tf
import json
from utils import checkmate as cm
from utils import data_helpers as dh
from utils import param_parser as parser
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, average_precision_score

args = parser.parameter_parser()
MODEL = dh.get_model_name()
logger = dh.logger_fn("tflog", "logs/Test-{0}.log".format(time.time()))

CPT_DIR = 'runs/' + MODEL + '/checkpoints/'
BEST_CPT_DIR = 'runs/' + MODEL + '/bestcheckpoints/'
SAVE_DIR = 'output/' + MODEL


def create_input_data(data: dict):
    return zip(data['pad_seqs'], data['onehot_labels'], data['labels'])

def bitqueryAPICall(query: str,variables:str):
    headers = {'X-API-KEY': 'BQYMlGZXUMMzcPCkoJ4Egn7aMVHOJuzu'}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query, 'variables': variables}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,query))

query = """
query ($network: EthereumNetwork!, $hash: String!, $limit: Int!, $offset: Int!) {
  ethereum(network: $network) {
    smartContractCalls(
      txHash: {is: $hash}
      options: {limit: $limit, offset: $offset}
    ) {
      smartContract {
        address {
          address
        }
      }
      smartContractMethod(smartContractMethod: {}) {
        name
      }
      address: caller {
        address
      }
    }
  }
}

"""



def test_crnn(tx_hash):
    client = pymongo.MongoClient(host='localhost',
                                 port=27017,
                                 #username='admin',
                                 #password='123456'
                                 )
    db = client.get_database('geth')
    tx = db.get_collection('transaction')
    hs = db.get_collection('transaction')
    def show(document):
        for d in document:
            print(d)
    i = 0
    with open('../data/test1.txt', 'a') as f:
        f.truncate(0)
    for tx in tx.find({"tx_hash":tx_hash}, {"tx_trace": 1, "_id": 0}):
        i = i + 1
        with open('../data/test1.txt', 'a') as f:
            f.write(tx.get('tx_trace'))
            f.write('\n')
        if (i == 2):
            break
    j = 0
    with open('../data/tx_hash1.txt', 'a') as f:
        f.truncate(0)
    for hs in hs.find({"tx_hash":tx_hash}, {"tx_hash": 1, "_id": 0}):
        j = j + 1
        with open('../data/tx_hash1.txt', 'a') as f:
            f.write(hs.get('tx_hash'))
            f.write('\n')
        if (j == 2):
            break



    data_file = "../data/test1.txt"
    label_file = "../data/label1.txt"


    test_file = "../data/test1.json"

    d_f = open(data_file, "r", encoding="utf-8")
    l_f = open(label_file, "r", encoding="utf-8")

    test_f = open(test_file, "w", encoding="utf-8")
    index = 0

    while True:
        data = d_f.readline()
        label = l_f.readline()
        dic = dict()
        if data and label:
            data_arr = data.strip().split(" ")
            label_arr = label.strip()[1:-1].split(",")
            label_list = []
            for i, l in enumerate(label_arr):
                if l == '1':
                    label_list.append(str(i))
            dic["testid"] = str(index)
            dic["features_content"] = data_arr
            dic["labels_index"] = label_list
            dic["labels_num"] = len(label_list)
            json_str = json.dumps(dic)
            #random_value = random.random()
            test_f.write(json_str + "\n")
            index += 1
        else:
            break
    test_f.close()
    """Test CRNN model."""
    # Print parameters used for the model
    dh.tab_printer(args, logger)

    # Load word2vec model
    # word2idx, embedding_matrix = dh.load_word2vec_matrix(args.word2vec_file)

    # custom
    word2idx = dh.get_word_index(args.word_idx_file)
    embedding_matrix = None

    # Load data
    logger.info("Loading data...")
    logger.info("Data processing...")
    test_data = dh.load_data_and_labels(args, "../data/test1.json", word2idx)

    # Load crnn model
    OPTION = dh._option(pattern=1)
    if OPTION == 'B':
        logger.info("Loading best model...")
        checkpoint_file = cm.get_best_checkpoint(BEST_CPT_DIR, select_maximum_value=True)
    else:
        logger.info("Loading latest model...")
        checkpoint_file = tf.train.latest_checkpoint(CPT_DIR)
    logger.info(checkpoint_file)

    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
            allow_soft_placement=args.allow_soft_placement,
            log_device_placement=args.log_device_placement)
        session_conf.gpu_options.allow_growth = args.gpu_options_allow_growth
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{0}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            input_y = graph.get_operation_by_name("input_y").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
            is_training = graph.get_operation_by_name("is_training").outputs[0]

            # Tensors we want to evaluate
            scores = graph.get_operation_by_name("output/scores").outputs[0]
            loss = graph.get_operation_by_name("loss/loss").outputs[0]

            # Split the output nodes name by '|' if you have several output nodes
            output_node_names = "output/scores"

            # Save the .pb model file
            output_graph_def = tf.graph_util.convert_variables_to_constants(sess, sess.graph_def,
                                                                            output_node_names.split("|"))
            tf.train.write_graph(output_graph_def, "graph", "graph-crnn-{0}.pb".format(MODEL), as_text=False)

            # Generate batches for one epoch
            batches = dh.batch_iter(list(create_input_data(test_data)), args.batch_size, 1, shuffle=False)

            # Collect the predictions here
            test_counter, test_loss = 0, 0.0
            test_pre_tk = [0.0] * args.topK
            test_rec_tk = [0.0] * args.topK
            test_F1_tk = [0.0] * args.topK

            # Collect the predictions here
            true_labels = []
            predicted_labels = []
            predicted_scores = []
            max_score=[]

            # Collect for calculating metrics
            true_onehot_labels = []
            predicted_onehot_scores = []
            predicted_onehot_labels_ts = []
            predicted_onehot_labels_tk = [[] for _ in range(args.topK)]

            for batch_test in batches:
                x, y_onehot, y = zip(*batch_test)
                feed_dict = {
                    input_x: x,
                    input_y: y_onehot,
                    dropout_keep_prob: 1.0,
                    is_training: False
                }

                batch_scores, cur_loss = sess.run([scores, loss], feed_dict)

                # Prepare for calculating metrics
                for i in y_onehot:
                    true_onehot_labels.append(i)
                for j in batch_scores:
                    predicted_onehot_scores.append(j)

                # Get the predicted labels by threshold
                batch_predicted_labels_ts, batch_predicted_scores_ts = \
                    dh.get_label_threshold(scores=batch_scores, threshold=args.threshold)

                # Add results to collection
                for i in y:
                    true_labels.append(i)
                for j in batch_predicted_labels_ts:
                    predicted_labels.append(j)
                for k in batch_predicted_scores_ts:
                    predicted_scores.append(k)
                    max_score.append(max(k))
                    #for l in k :
                        #if l > 0.5:
                            #max_score.append(l)
                #print(max_score)
                #print(len(max_score))
                plt.hist(max_score, 40)
                plt.xlabel('Probability')
                plt.ylabel('Frequency')
                plt.title("Distribution of the maximum probability of the five labels")
                plt.axis([0, 2, 0, 100])
                #plt.show()

                # Get onehot predictions by threshold
                batch_predicted_onehot_labels_ts = \
                    dh.get_onehot_label_threshold(scores=batch_scores, threshold=args.threshold)
                for i in batch_predicted_onehot_labels_ts:
                    predicted_onehot_labels_ts.append(i)

                # Get onehot predictions by topK
                for top_num in range(args.topK):
                    batch_predicted_onehot_labels_tk = dh.get_onehot_label_topk(scores=batch_scores, top_num=top_num+1)

                    for i in batch_predicted_onehot_labels_tk:
                        predicted_onehot_labels_tk[top_num].append(i)

                test_loss = test_loss + cur_loss
                test_counter = test_counter + 1

            # Calculate Precision & Recall & F1
            #test_pre_ts = precision_score(y_true=np.array(true_onehot_labels),
                                          #y_pred=np.array(predicted_onehot_labels_ts), average='micro')
            #test_rec_ts = recall_score(y_true=np.array(true_onehot_labels),
                                       #y_pred=np.array(predicted_onehot_labels_ts), average='micro')
            #test_F1_ts = f1_score(y_true=np.array(true_onehot_labels),
                                  #y_pred=np.array(predicted_onehot_labels_ts), average='micro')

            #for top_num in range(args.topK):
                #test_pre_tk[top_num] = precision_score(y_true=np.array(true_onehot_labels),
                                                       #y_pred=np.array(predicted_onehot_labels_tk[top_num]),
                                                       #average='micro')
                #test_rec_tk[top_num] = recall_score(y_true=np.array(true_onehot_labels),
                                                    #y_pred=np.array(predicted_onehot_labels_tk[top_num]),
                                                    #average='micro')
                #test_F1_tk[top_num] = f1_score(y_true=np.array(true_onehot_labels),
                                               #y_pred=np.array(predicted_onehot_labels_tk[top_num]),
                                               #average='micro')

            # Calculate the average AUC
            #test_auc = roc_auc_score(y_true=np.array(true_onehot_labels),
                                                       # y_score=np.array(predicted_onehot_scores), average='micro')

            # Calculate the average PR
            #test_prc = average_precision_score(y_true=np.array(true_onehot_labels),
                                               #y_score=np.array(predicted_onehot_scores), average="micro")
            #test_loss = float(test_loss / test_counter)

            #logger.info("All Test Dataset: Loss {0:g} | AUC {1:g} | AUPRC {2:g}"
                        #.format(test_loss, test_auc, test_prc))

            # Predict by threshold
            #logger.info("Predict by threshold: Precision {0:g}, Recall {1:g}, F1 {2:g}"
                        #.format(test_pre_ts, test_rec_ts, test_F1_ts))

            # Predict by topK
            #logger.info("Predict by topK:")
            #for top_num in range(args.topK):
                #logger.info("Top{0}: Precision {1:g}, Recall {2:g}, F1 {3:g}"
                            #.format(top_num + 1, test_pre_tk[top_num], test_rec_tk[top_num], test_F1_tk[top_num]))

            # Save the prediction result
            if not os.path.exists(SAVE_DIR):
                os.makedirs(SAVE_DIR)
            dh.create_prediction_file(output_file=SAVE_DIR + "/predictions.json", data_id=test_data['id'],
                                      true_labels=true_labels, predict_labels=predicted_labels,
                                      predict_scores=predicted_scores)

    logger.info("All Done.")
    i=0
    vul=[]
    labell=[]
    for lis in predicted_scores:
       i=i+1
       if max(lis)>0.5:
           #print(sum(lis))
           #print(lis)
           labell.append(lis.index(max(lis)))
           vul.append(i)

    #print(vul)
    #print(len(vul))
    count=0
    index=-1
    mingcheng=[]
    txhash=[]
    for lab in labell:
        if(lab==0):
            mingcheng.append("Incorrect Check for Authorization")
        if(lab==1):
            mingcheng.append("No Check after Contract Invocation")
        if (lab == 2):
            mingcheng.append("Missing the Transfer Event ")
        if (lab == 3):
            mingcheng.append("Strict Check for Balance ")
        if (lab == 4):
            mingcheng.append("Timestamp Dependency & Block Number Dependency")

    file_object1 = open("../data/tx_hash1.txt", 'r')
    try:
        with open("../data/result.txt", 'a') as f:
            f.truncate(0)
        while True:
            line = file_object1.readline()
            count=count+1
            if (line and vul.__contains__(count)):
                with open("../data/result.txt", 'a') as f:
                    index=index+1
                    f.write(mingcheng[index]+',')
                    f.write(line)
                    txhash.append(line)
            elif (line==""):
                break
            else:
                continue
    finally:
        file_object1.close()
        #print(count)
    #print(len(vul))
    dic = dict()
    dic["txhash"] = tx_hash
    if(index==-1):
        dic["mingcheng"] = "No vulnerability";
    else:
        dic["mingcheng"] = mingcheng[index];
    variables = {
            "limit": 10,
            "offset": 0,
            "network": "ethereum",
            "hash": tx_hash
        }
    address=[]
    result = bitqueryAPICall(query,variables)
    # inflow = result['data']['bitcoin']['inputs'][0]['value']
    # outflow = result['data']['bitcoin']['outputs'][0]['value']
    # balance = outflow-inflow
    # print ("The balance of the Bitcoin wallet is {}".format(balance))
    print(result)
    result['data']['ethereum']['smartContractCalls'][0]['address']['address']=""
    for name in result['data']['ethereum']['smartContractCalls']:
        if name['address']['address'] == "":
            address.append(name['smartContract']['address']['address'])
        else:
            address.append(name['address']['address'])
            address.append(name['smartContract']['address']['address'])

    #print(type(result))
    dic["address"]=list(set(address))
    #logger.info(json.dumps(dic))
    return json.dumps(dic)



#if __name__ == '__main__':

    #test_crnn()
