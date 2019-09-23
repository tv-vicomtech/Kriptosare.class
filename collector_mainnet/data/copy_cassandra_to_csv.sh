#!/bin/bash
COPY blockchain_data.transaction to 'transaction.csv' with header=true;
COPY blockchain_data.block to 'block.csv' with header=true;
