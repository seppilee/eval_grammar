


#!/usr/bin/python
#-*- coding: UTF-8 -*-

"""Example of a translation client."""
from __future__ import print_function

import argparse
import pyonmttok
import sys
import tensorflow as tf
import codecs
import grpc
import numpy
import itertools
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc


def get_lines(filepath_with_name):
    lines = []
    with codecs.open(filepath_with_name, encoding="utf-8") as f:
        for line in f:
            lines.append(line.strip().split())
    return lines

def split_seq(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))

def pad_batch(batch_tokens):
  """Pads a batch of tokens."""
  lengths = [len(tokens) for tokens in batch_tokens]
  max_length = max(lengths)
  for tokens, length in zip(batch_tokens, lengths):
    if max_length > length:
      tokens += [""] * (max_length - length)
  return batch_tokens, lengths, max_length


def extract_prediction(result):
  """Parses a translation result.
  Args:
    result: A `PredictResponse` proto.

  Returns:
    A generator over the hypotheses.
  """
  batch_lengths = tf.make_ndarray(result.outputs["length"])
  batch_predictions = tf.make_ndarray(result.outputs["tokens"])
  for hypotheses, lengths in zip(batch_predictions, batch_lengths):
    # Only consider the first hypothesis (the best one).
    best_hypothesis = hypotheses[0]
    best_length = lengths[0] - 1  # Ignore </s>
    yield best_hypothesis[:best_length]
yield best_hypothesis[:best_length]

def send_request(stub, model_name, batch_tokens, timeout=5.0):
  """Sends a translation request.

  Args:
    stub: The prediction service stub.
    model_name: The model to request.
    tokens: A list of tokens.
    timeout: Timeout after this many seconds.

  Returns:
    A future.
  """
  batch_tokens, lengths, max_length = pad_batch(batch_tokens)
  batch_size = len(lengths)
  request = predict_pb2.PredictRequest()
  request.model_spec.name = model_name
  request.inputs["tokens"].CopyFrom(
      tf.make_tensor_proto(batch_tokens, shape=(batch_size, max_length)))
  request.inputs["length"].CopyFrom(
      tf.make_tensor_proto(lengths, shape=(batch_size,)))
  return stub.Predict.future(request, timeout)

def translate(stub, model_name, batch_text, tokenizer, timeout=5.0):
  """Translates a batch of sentences.

  Args:
    stub: The prediction service stub.
    model_name: The model to request.
    batch_text: A list of sentences.
    tokenizer: The tokenizer to apply.
    timeout: Timeout after this many seconds.

  Returns:
    A generator over the detokenized predictions.
  """
  #batch_input = [tokenizer.tokenize(text)[0] for text in batch_text]
  #batch_input = [text.split() for text in batch_text]
  batch_input = split_seq(range(0, len(batch_text)+1), 32)
  batch_input = list(batch_input)
  #print(batch_input[0][0],batch_input[0][-1])
  for x in range(len(batch_input)):
      future = send_request(stub, model_name, batch_text[batch_input[x][0]:batch_input[x][-1]], timeout=timeout)
      result = future.result()

      batch_output = (prediction for prediction in extract_prediction(result))
      yield batch_output
  #batch_outputs.extend(batch_output)
  #batch_output = [tokenizer.detokenize(prediction) for prediction in extract_prediction(result)]
  #return batch_output

def main():
  parser = argparse.ArgumentParser(description="Translation client example")
  parser.add_argument("--model_name", required=True,
                      help="model name")
  parser.add_argument("--sentencepiece_model", default="",
                      help="path to the sentence model")
 parser.add_argument("--sentencepiece_model", default="",
                      help="path to the sentence model")
  parser.add_argument("--host", default="localhost",
                      help="model server host")
  parser.add_argument("--port", type=int, default=9000,
                      help="model server port")
  parser.add_argument("--timeout", type=float, default=10.0,
                      help="request timeout")
  parser.add_argument('--input', required=True,  help="The input file.")
  args = parser.parse_args()

  channel = grpc.insecure_channel("%s:%d" % (args.host, args.port))
  stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
  tokenizer = pyonmttok.Tokenizer("none", sp_model_path=args.sentencepiece_model)

  input_file = args.input
  batch_input = get_lines(input_file)
  #batch_input = ["限@@ 三百@@ 張 , 許@@ 賣@@ 恐@@ 宜 。", "當初@@ 李承@@ 已@@ 知@@ 而言之 。"]
  batch_output = translate(stub, args.model_name, batch_input, tokenizer, timeout=args.timeout)
  for batch_output1 in batch_output:
      for batch_output2 in batch_output1:
          ret = " ".join(str(batch_output3.decode('UTF-8')) for batch_output3 in batch_output2)
          print(ret.replace("@@ ",""))
      #for input_text, output_text in zip(batch_input,batch_output1):
      #print("{} ||| {}".format(input_text, output_text.decode()))

if __name__ == "__main__":
  main()
