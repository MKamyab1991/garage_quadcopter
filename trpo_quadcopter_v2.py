#!/usr/bin/env python3
"""This is an example to train a task with TRPO algorithm (PyTorch).

Here it runs InvertedDoublePendulum-v2 environment with 100 iterations.
"""
import torch

from garage import wrap_experiment
from garage.envs import GymEnv
from garage.experiment.deterministic import set_seed
from garage.sampler import LocalSampler
from garage.torch.algos import TRPO
from garage.torch.policies import GaussianMLPPolicy
from garage.torch.value_functions import GaussianMLPValueFunction
from garage.trainer import Trainer
import gym
import envs

@wrap_experiment(archive_launch_repo=False)
def trpo_quadcopter(ctxt=None, seed=1):
    """Train TRPO with InvertedDoublePendulum-v2 environment.

    Args:
        ctxt (garage.experiment.ExperimentContext): The experiment
            configuration used by Trainer to create the snapshotter.
        seed (int): Used to seed the random number generator to produce
            determinism.

    """
    set_seed(seed)
    fake_env = gym.make("CustomEnv-v0")
    env = GymEnv("CustomEnv-v0", max_episode_length=fake_env.numTimeStep)

    trainer = Trainer(ctxt)

    policy = GaussianMLPPolicy(
        env.spec, hidden_sizes=(200, 200), hidden_nonlinearity=torch.relu, output_nonlinearity=torch.tanh
    )

    value_function = GaussianMLPValueFunction(
        env_spec=env.spec, hidden_sizes=(200, 200), hidden_nonlinearity=torch.relu, output_nonlinearity=torch.tanh
    )

    sampler = LocalSampler(agents=policy, envs=env, max_episode_length=env.spec.max_episode_length)

    algo = TRPO(
        env_spec=env.spec,
        policy=policy,
        value_function=value_function,
        sampler=sampler,
        discount=0.995,
        center_adv=False,
    )

    trainer.setup(algo, env)
    trainer.train(n_epochs=100, batch_size=1024)


trpo_quadcopter(seed=1)
