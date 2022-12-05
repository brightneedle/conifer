import util
import numpy as np
import conifer
import json

'''
Test conifer's model saving and loading functionality by loading some models and checking the predictions
match the original.
'''
def test_hls_save_load(hls_convert, train_skl):
  orig_model = hls_convert
  clf, X, y = train_skl
  load_model = conifer.model.load_model(f'{orig_model.config["OutputDir"]}/my_prj.json')
  load_model.config['OutputDir'] += '_loaded'
  load_model.compile()
  y_hls_0, y_hls_1 = util.predict_skl(orig_model, X, y, load_model)
  np.testing.assert_array_equal(y_hls_0, y_hls_1)

def test_hdl_save_load(vhdl_convert, train_skl):
  orig_model = vhdl_convert
  clf, X, y = train_skl
  load_model = conifer.model.load_model(f'{orig_model.config["OutputDir"]}/my_prj.json')
  load_model.config['OutputDir'] += '_loaded'
  load_model.compile()
  y_hdl_0, y_hdl_1 = util.predict_skl(orig_model, X, y, load_model)
  np.testing.assert_array_equal(y_hdl_0, y_hdl_1)

def test_new_config(hls_convert, train_skl):
  orig_model = hls_convert
  clf, X, y = train_skl
  with open(f'{orig_model.config["OutputDir"]}/my_prj.json') as json_file:
    js = json.load(json_file)
  cfg = js['config']
  cfg['Backend'] = 'cpp'
  cfg['OutputDir'] += '_loaded'
  load_model = conifer.model.load_model(f'{orig_model.config["OutputDir"]}/my_prj.json', new_config=cfg)
  load_model.compile()
  y_hls_0, y_cpp_1 = util.predict_skl(orig_model, X, y, load_model)
  np.testing.assert_array_equal(y_hls_0, y_cpp_1.reshape(y_hls_0.shape))