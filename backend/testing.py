# import os, json

# if not os.path.isfile('cec_data.json'):
#     with open('cec_data.json', 'w') as f:
#         json.dump({}, f, indent=4)

cec_score = {'18602a6895ea4bd8b056f0d1c72966fb': 202.0, '6f5ba59c53d84b1e84ab6c70af93349f': 198.0}
for alg in cec_score:
    print(alg)
    print(cec_score[alg])
    # session.commit()