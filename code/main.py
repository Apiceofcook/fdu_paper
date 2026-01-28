import argparse

import tool.generate_v22
# from tool.generate_v20 import API_GEN
import tool.filtration_v12
# from tool.filtration_v10 import API_Filter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='')
    parser.add_argument('--dataset_key', type=str, default='')
    parser.add_argument('--origin_file', type=str, default='')
    parser.add_argument('--API_keys', type=list, default=[])
    parser.add_argument('--Con_num', type=int, default=1)
    parser.add_argument('--Step', type=int, default=1)
    parser.add_argument('--IF_CAP', type=bool, default=False)
    parser.add_argument('--IF_REC', type=bool, default=False)
    parser.add_argument('--IF_MERGE', type=bool, default=False)
    parser.add_argument('--IF_RELEVANCE', type=bool, default=False)
    parser.add_argument('--IF_RULE', type=bool, default=False)
    parser.add_argument('--temperature', type=float, default=1)
    args = parser.parse_args()


    # caption
    if args.Step > 0:
        print("-------------Caption Generate-------------")
        args.IF_CAP = True
        args.IF_REC = False
        args.IF_MERGE = False
        tool.generate_v22.API_GEN(args)

    # relevance filter
    if args.Step > 1:
        print("-------------Relevance Filter-------------")
        args.IF_RELEVANCE = True
        args.IF_RULE = False
        tool.filtration_v12.API_Filter(args)

    # rec,know,fianl
    if args.Step > 2:
        print("-------------QA Generate-------------")
        args.IF_CAP = False
        args.IF_REC = True
        args.IF_MERGE = True
        tool.generate_v22.API_GEN(args)

    # rule filter
    if args.Step > 3:
        print("-------------Rule Filter-------------")
        args.IF_RELEVANCE = False
        args.IF_RULE = True
        tool.filtration_v11.API_Filter(args)
