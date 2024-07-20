# Growing islands to approximate tessellations of the plane by Voronoi diagrams

BSc Thesis Maastricht University, "Data Science & Artificial Intelligence", 2023

**Usage**: Refer to the [Just](https://github.com/casey/just)file. Run `just` to see all available commands.

**Project Modules**:
- **diagram-tracer**: Program to draw tessellations over images
- **growing-islands**: Central thesis codebase
- **thesis-experiments**: Scripts to run experiments and generate plots used in the thesis

![](misc/images/growing.gif)
___

### Abstract

> _Voronoi diagrams are well-studied objects in the field of computational geometry. One problem related to Voronoi diagrams is the Inverse Voronoi problem where, given a tessellation of the plane into convex regions, we wish to find the points which could have generated the tessellation. Sometimes this is not possible, but it can be desirable to approximate the original tessellation by a Voronoi diagram. This paper presents a new algorithm for generating these approximations using a proposed definition for ”Voronoi-ness” of arbitrary tessellations, previously not well-defined in the literature. The results show that the algorithm does well on tessellations with mostly well-shaped and uniformly sized regions. The algorithm also marginally improves an existing solution for the approximation of territories of Tilapia mossambica by a Voronoi tessellation from 3.8% to 3.08%._


📃 Details & results can be found in the [paper](report.pdf).

*This thesis received a grade of 9.0 (out of 10) in the Dutch grading system.*
