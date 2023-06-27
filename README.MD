# Growing islands to approximate tessellations of the plane by Voronoi diagrams

BSc Thesis "Data Science & Artificial Intelligence", 2023

_Voronoi diagrams are well-studied objects in the field of computational geometry. One problem related to Voronoi diagrams is the Inverse Voronoi Problem where, given a tessellation of convex regions, we wish to find the points which could have generated the tessellation. Sometimes this is not possible however, and we may not know if such a set of points can even be found, hence it is desirable to approximate the original tessellation by a Voronoi diagram. This research presents a new algorithm for generating these approximations using a proposed definition for ”Voronoi-ness” of arbitrary tessellations, previously not well-defined in the literature. Optimal parameters for the algorithm were deduced experimentally, and the results show that the algorithm does well on tessellations with mostly well-shaped and uniformly sized regions, as well as yielding a marginally better approximation for the territories of Tilapia mossambica than a previous paper._

![](images/growing.gif)

## Dependencies
- matplotlib v3.7.1
- shapely v2.0.1
- geopandas v0.13.1

## References
- _Narciso Aguilera, Belen Palop, and Hebert P´erez-Ros´es. Approximating imprecise planar tesselations with voronoi diagrams. In Proceedings of VISUAL 2016, pages 19–23, 11 2016._
- _Peter F. Ash and Ethan D. Bolker. Recognizing dirichlet tessellations. Geometriae Dedicata, 19:175–206, 1985._
- _George W. Barlow. Hexagonal territories. Animal Behaviour, 22:876–IN1, 1974._
- _Jon Louis Bentley and Jerome H. Friedman. Data structures for range searching. ACM Comput. Surv., 11(4):397–409, dec 1979._
- _Emden R. Gansner, Yehuda Koren, and Stephen C. North. Graph drawing by stress majorization. In International Symposium Graph Drawing and Network Visualization, 2004._
- _Masami Hasegawa and Masaharu Tanemura. On the pattern of space division by territories. Annals of the Institute of Statistical Mathematics, 28:509–519, 02 1976._
- _David Heath and Simon Kasif. The complexity of finding minimal voronoi covers with applications to machine learning. Computational Geometry, 3(5):289–305, 1993._
- _Hisao Honda. Description of cellular patterns by dirichlet domains: The two-dimensional case. Journal of Theoretical Biology, 72(3):523–543, June 1978._
- _Atsuo Suzuki and Masao Iri. Approximation of a tessellation of the plane by a voronoi diagram. Journal of the Operations Research Society of Japan, 29(1):69–97, 1986._
