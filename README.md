# Project
NOTE: We are in the process of migrating the code from here: https://github.com/ryu577/graphing. Until you see this message, please use that repository.

> This repo has been populated by an initial template to help get you started. Please
> make sure to update the content to build a great experience for community-building.

As the maintainer of this project, please make a few updates:

- Improving this README.MD file to provide a great experience
- Updating SUPPORT.MD with content about this project's support experience
- Understanding the security reporting process in SECURITY.MD
- Remove this section from the README

# Usage
To install the library on your local machine, clone it and run from the base directory:

> python setup.py install

Then, try to run the following sample code:

> from graphing.special_graphs.neural_trigraph.path_cover import min_cover_trigraph
> 
> from graphing.special_graphs.neural_trigraph.rand_graph import *
> ## Generate a random neural trigraph. Here, it is two sets of edges between layers 1 and 2 (edges1) and layers 2 and 3 (edges2)
> edges1, edges2 = neur_trig_edges(7, 3, 7, shuffle_p=.05)
> ## Find the full-path cover for this neural trigraph.
> paths1 = min_cover_trigraph(edges1, edges2)
> 
> print(paths1)


## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
