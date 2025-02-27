import argparse
from sklearn.model_selection import ParameterGrid
import copy
import os

parser = argparse.ArgumentParser(description='Taking commands for the Protein Generator')
parser.add_argument('experiment_base_name', type=str, action='store', nargs=1, 
                    help='Name to use for the experiment directory of outputs')
parser.add_argument('--run_model', type=str, action='store', nargs='+', 
                    default=['evCouplings.py'],
                    help='select the model run script to use for training. Currently only EV Couplings. ')
parser.add_argument('--protein_length', type=int, action='store', nargs='+',
                    default = [0],
                    help='Can trim the size of the protein loaded in for \
                        faster testing and training. 0 means no trimming')
parser.add_argument('--MLepochs', type=int, action='store', nargs='+',
                    default = [300],
                    help='Number of Epochs for pure ML training. If set to 0 then it skips ML training')
parser.add_argument('--KLepochs', type=int, action='store', nargs='+',
                    default = [500],
                    help='Number of Epochs for ML and KL training')
parser.add_argument('--lr', type=float, action='store', nargs='+',
                    default = [0.001],
                    help='Learning Rate for both ML and KL')
parser.add_argument('--tda', type=int, action='store', nargs='+',
                    default = [2000],
                    help='training data amount. Will assert that it is less than the total amount of data. \
                        Currently also splits this equally and randomly into train and test')            
parser.add_argument('--MLbatch', type=int, action='store', nargs='+',
                    default = [124],
                    help='Batchsize for ML')
parser.add_argument('--KLbatch', type=int, action='store', nargs='+',
                    default = [124],
                    help='Batchsize for KL')
parser.add_argument('--temperature', type=float, action='store', nargs='+',
                    default = [1.0],
                    help='temperature used to sample from the latent (can introduce more std)')
parser.add_argument('--explore', type=float, action='store', nargs='+',
                    default = [1.0],
                    help='exploration to prevent mode collapse')
parser.add_argument('--latent_std', type=float, action='store', nargs='+',
                    default = [1.0],
                    help='latent space standard deviation of the normal')
parser.add_argument('--MLweight', type=float, action='store', nargs='+',
                    default = [1.0],
                    help='Number of Epochs for pure ML training')
parser.add_argument('--Entropyweight', type=float, action='store', nargs='+',
                    default = [1.0],
                    help='The amount of entropy penalty to the generated sequences.')
parser.add_argument('--KLweight', type=float, action='store', nargs='+',
                    default = [1.0],
                    help='Number of Epochs for pure ML training')
parser.add_argument('--save_partway_inter', type=float, action='store', nargs=1,
                    default = [None],
                    help='Number of epochs want to save the model during as a percentage of the total number of epochs')
parser.add_argument('--model_architecture', type=str, action='store', nargs='+',
                    default = ['NNNNNS'],
                    help='type of invertible network. N NICER layer \n \
                    n NICER layer, share parameters with last layer \
                    R RealNVP layer \
                    r RealNVP layer, share parameters with last layer \
                    S Scaling layer \
                    W Whiten layer \
                    P Permute layer \
                    Z Split dimensions off to latent space, leads to a merge and 3-way split. \
                    Splitting and merging layers will be added automatically')
parser.add_argument('--nl_activation', type=str, action='store', nargs='+',
                    default = ['relu'],
                    help='type of activation for all but scaling layers')
parser.add_argument('--verbose', type=bool, action='store', nargs='+',
                    default = [True],
                    help='type of activation for all but scaling layers')
parser.add_argument('--KL_only', type=bool, action='store', nargs='+',
                    default = [False],
                    help='rather than joint, do KL training only')
parser.add_argument('--dequantize', type=bool, action='store', nargs='+',
                    default = [False],
                    help='dequantize the training data')
parser.add_argument('--nl_activation_scale', type=str, action='store', nargs='+',
                    default = ['tanh'],
                    help='type of activation for scaling')
parser.add_argument('--gradient_clip', type=float, action='store', nargs='+',
                    default = [1.0],
                    help='amount of gradient clipping')
parser.add_argument('--load_model', type=str, action='store', nargs='+',
                    default = ['None'],
                    help='give the correct path to load in the model')
parser.add_argument('--random_seed', type=int, action='store', nargs='+',
                    default = [27],
                    help='the random seed used')

args = parser.parse_args()
run_model_str = args.run_model[0]
print('Commmand line args are:', args)
arg_dict = copy.deepcopy(vars(args))
tot_combos = 1
for v in arg_dict.values():
    tot_combos *= len(v)
pg = ParameterGrid(arg_dict)
print(args.run_model)
if run_model_str == 'evCouplings.py':
    from evCouplings import main
    func_to_call = main
'''elif run_model_str == 'basic_evCouplings.py':
    from basic_evCouplings import main
    func_to_call = main'''
for i in range(tot_combos):
    print(' ====================== Running param combo ', i, '/', tot_combos, '======================')
    print('combo of params is:', pg[i])

    func_to_call( pg[i])
