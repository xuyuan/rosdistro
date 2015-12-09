'''copy previous setup to new ubuntu release for rosdistro yaml files.
Example: python upgrade_rosdistro.py vivid rosdep/base.yaml wily rosdep/new_base.yaml
'''


import yaml
import argparse
import copy


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('input_release', type=str, nargs=1, help='ubuntu release name to be copied from')
parser.add_argument('input', type=str, nargs=1, help='original yaml file')
parser.add_argument('output_release', type=str, nargs=1, help='ubuntu release name to be copied to')
parser.add_argument('output', type=str, nargs=1, help='new yaml file')
args = parser.parse_args()

input_release = args.input_release[0]
output_release = args.output_release[0]

data = yaml.load(open(args.input[0]))
for pkg_name, pkg_data in data.iteritems():
    for sys_name, sys_data in pkg_data.iteritems():
        if sys_name == 'ubuntu':
            if isinstance(sys_data, dict):
                # ubuntu release matters
                if output_release not in sys_data and input_release in sys_data:
                    print 'copy', pkg_name, sys_data[input_release]
                    sys_data[output_release] = copy.deepcopy(sys_data[input_release])

with open(args.output[0], 'w') as f:
    f.write(yaml.dump(data))
