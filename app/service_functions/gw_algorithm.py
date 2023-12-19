# ******************************************************************************
#  Copyright (c) 2020 University of Stuttgart
#
#  See the NOTICE file(s) distributed with this work for additional
#  information regarding copyright ownership.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************

import networkx as nx
import cvxgraphalgs as cvxgr
import numpy as np


def best_gw_cuts(graph, n_GW_cuts, rounded=False):
    np_graph_array = np.array(graph)
    nx_graph = nx.from_numpy_matrix(np_graph_array)

    gw_cuts = []
    for i in range(n_GW_cuts):
        approximation = cvxgr.algorithms.goemans_williamson_weighted(nx_graph)

        # compute binary representation of cut for discrete solution
        approximation_list_rounded = ""
        for n in range(len(approximation.vertices)):
            if n in approximation.left:
                approximation_list_rounded += "0"
            else:
                approximation_list_rounded += "1"

        if not gw_cuts or not (
            approximation_list_rounded in list(np.array(gw_cuts, dtype=object)[:, 0])
        ):
            gw_cuts.append(
                [approximation_list_rounded, approximation.evaluate_cut_size(nx_graph)]
            )

    # return n_best best cuts
    gw_cuts = np.array(gw_cuts, dtype=object)
    gw_cuts = gw_cuts[gw_cuts[:, 1].argsort()]
    gw_cuts = gw_cuts[-1:]
    return gw_cuts[0][0], gw_cuts[0][1]
