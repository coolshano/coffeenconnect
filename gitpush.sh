#!/bin/bash
# ============================
# My First Shell Script
# Author: Shannon Smith
# Description: Git push script
# ============================

git add .

echo "Enter commit message"
read commit

git commit -m "$commit"

git push --set-upstream origin main --force


