#!/usr/bin/env bash
# Runs the genetic algorithm training loop
cd "$(dirname "$0")"
virtual_environment/bin/python -m model_and_training.training_loop_genetics_pygame
