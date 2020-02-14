import subprocess
import madrob_beast_pi.madrob
from madrob_beast_pi.madrob import *
import madrob_beast_pi.beast
from madrob_beast_pi.beast import *

print('\n-----\nBuilding docker images for every PI.\n-----\n')

benchmark_type='madrob'
for pi_name in madrob_beast_pi.madrob.__all__:
    print('\n----\nBuilding image for %s\n----\n' % pi_name)
    subprocess.call(['sudo', 'docker', 'build', '--build-arg', 'BENCHMARK_TYPE=%s' % (benchmark_type), '--build-arg', 'PI_NAME=%s' % (pi_name), '-t=%s_%s' % (benchmark_type, pi_name), '.'])

benchmark_type='beast'
for pi_name in madrob_beast_pi.beast.__all__:
    print('\n----\nBuilding image for %s\n----\n' % pi_name)
    subprocess.call(['sudo', 'docker', 'build', '--build-arg', 'BENCHMARK_TYPE=%s' % (benchmark_type), '--build-arg', 'PI_NAME=%s' % (pi_name), '-t=%s_%s' % (benchmark_type, pi_name), '.'])