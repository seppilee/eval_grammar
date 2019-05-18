#!/usr/bin/env python
import configargparse

from flask import Flask, jsonify, request
from onmt.translate import TranslationServer, ServerModelError

STATUS_OK = "ok"
STATUS_ERROR = "error"


class ServerModelError(Exception):
    pass

class TranslationServer(object):
    def __init__(self):
        self.models = {}
        self.next_id = 0

    def start(self, config_file):
        """Read the config file and pre-/load the models."""
        self.config_file = config_file
        with open(self.config_file) as f:
            self.confs = json.load(f)

        self.models_root = self.confs.get('models_root', './available_models')
        for i, conf in enumerate(self.confs["models"]):
            if "models" not in conf:
                if "model" in conf:
                    # backwards compatibility for confs
                    conf["models"] = [conf["model"]]
                else:
                    raise ValueError("""Incorrect config file: missing 'models'
                                        parameter for model #%d""" % i)
            kwargs = {'timeout': conf.get('timeout', None),
                      'load': conf.get('load', None),
                      'tokenizer_opt': conf.get('tokenizer', None),
                      'on_timeout': conf.get('on_timeout', None),
                      'model_root': conf.get('model_root', self.models_root)
                      }
            kwargs = {k: v for (k, v) in kwargs.items() if v is not None}
            model_id = conf.get("id", None)
            opt = conf["opt"]
            opt["models"] = conf["models"]
            self.preload_model(opt, model_id=model_id, **kwargs)

    def clone_model(self, model_id, opt, timeout=-1):
        """Clone a model `model_id`.
        Different options may be passed. If `opt` is None, it will use the
        same set of options
        """
        if model_id in self.models:
            if opt is None:
                opt = self.models[model_id].user_opt
            opt["models"] = self.models[model_id].opt.models
            return self.load_model(opt, timeout)
        else:
            raise ServerModelError("No such model '%s'" % str(model_id))

    def load_model(self, opt, model_id=None, **model_kwargs):
        """Load a model given a set of options
        """
        model_id = self.preload_model(opt, model_id=model_id, **model_kwargs)
        load_time = self.models[model_id].load_time

        return model_id, load_time

    def preload_model(self, opt, model_id=None, **model_kwargs):
        """Preloading the model: updating internal datastructure
        It will effectively load the model if `load` is set
        """
        if model_id is not None:
            if model_id in self.models.keys():
                raise ValueError("Model ID %d already exists" % model_id)
        else:
            model_id = self.next_id
            while model_id in self.models.keys():
                model_id += 1
            self.next_id = model_id + 1
        print("Pre-loading model %d" % model_id)
        model = ServerModel(opt, model_id, **model_kwargs)
        self.models[model_id] = model

        return model_id

    def run(self, inputs):
        """Translate `inputs`
        We keep the same format as the Lua version i.e.
        ``[{"id": model_id, "src": "sequence to translate"},{ ...}]``
        We use inputs[0]["id"] as the model id
        """

        model_id = inputs[0].get("id", 0)
        if model_id in self.models and self.models[model_id] is not None:
            return self.models[model_id].run(inputs)
        else:
            print("Error No such model '%s'" % str(model_id))
            raise ServerModelError("No such model '%s'" % str(model_id))

    def unload_model(self, model_id):
        """Manually unload a model.
        It will free the memory and cancel the timer
        """

        if model_id in self.models and self.models[model_id] is not None:
            self.models[model_id].unload()
        else:
            raise ServerModelError("No such model '%s'" % str(model_id))

    def list_models(self):
        """Return the list of available models
        """
        models = []
        for _, model in self.models.items():
            models += [model.to_dict()]
        return models

'''
main module
'''
def start(config_file,
          url_root="./translator",
          host="0.0.0.0",
          port=5000,
          debug=True):
    def prefix_route(route_function, prefix='', mask='{0}{1}'):
        def newroute(route, *args, **kwargs):
            return route_function(mask.format(prefix, route), *args, **kwargs)
        return newroute

    app = Flask(__name__)
    app.route = prefix_route(app.route, url_root)
    translation_server = TranslationServer()
    translation_server.start(config_file)

    @app.route('/models', methods=['GET'])
    def get_models():
        out = translation_server.list_models()
        return jsonify(out)

    @app.route('/clone_model/<int:model_id>', methods=['POST'])
    def clone_model(model_id):
        out = {}
        data = request.get_json(force=True)
        timeout = -1
        if 'timeout' in data:
            timeout = data['timeout']
            del data['timeout']

        opt = data.get('opt', None)
        try:
            model_id, load_time = translation_server.clone_model(
                model_id, opt, timeout)
        except ServerModelError as e:
            out['status'] = STATUS_ERROR
            out['error'] = str(e)
        else:
            out['status'] = STATUS_OK
            out['model_id'] = model_id
            out['load_time'] = load_time

        return jsonify(out)

    @app.route('/unload_model/<int:model_id>', methods=['GET'])
    def unload_model(model_id):
        out = {"model_id": model_id}

        try:
            translation_server.unload_model(model_id)
            out['status'] = STATUS_OK
        except Exception as e:
            out['status'] = STATUS_ERROR
            out['error'] = str(e)

        return jsonify(out)

    @app.route('/translate', methods=['POST'])
    def translate():
        inputs = request.get_json(force=True)
        out = {}
        try:
            translation, scores, n_best, times = translation_server.run(inputs)
            assert len(translation) == len(inputs)
            assert len(scores) == len(inputs)

            out = [[{"src": inputs[i]['src'], "tgt": translation[i],
                     "n_best": n_best,
                     "pred_score": scores[i]}
                    for i in range(len(translation))]]
        except ServerModelError as e:
            out['error'] = str(e)
            out['status'] = STATUS_ERROR

        return jsonify(out)

    @app.route('/to_cpu/<int:model_id>', methods=['GET'])
    def to_cpu(model_id):
        out = {'model_id': model_id}
        translation_server.models[model_id].to_cpu()

        out['status'] = STATUS_OK
        return jsonify(out)

    @app.route('/to_gpu/<int:model_id>', methods=['GET'])
    def to_gpu(model_id):
        out = {'model_id': model_id}
        translation_server.models[model_id].to_gpu()

        out['status'] = STATUS_OK
        return jsonify(out)

    app.run(debug=debug, host=host, port=port, use_reloader=False,
            threaded=True)


def _get_parser():
    parser = configargparse.ArgumentParser(
        config_file_parser_class=configargparse.YAMLConfigFileParser,
        description="OpenNMT-py REST Server")
    parser.add_argument("--ip", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default="5000")
    parser.add_argument("--url_root", type=str, default="/translator")
    parser.add_argument("--debug", "-d", action="store_true")
    parser.add_argument("--config", "-c", type=str,
                        default="./available_models/conf.json")
    return parser


if __name__ == '__main__':
    parser = _get_parser()
    args = parser.parse_args()
    start(args.config, url_root=args.url_root, host=args.ip, port=args.port,
          debug=args.debug)

