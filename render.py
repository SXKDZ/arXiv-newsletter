from flask import Flask, render_template
app = Flask(__name__)

newsletter = {
    'index': 1,
    'today': 'June 14, 2022',
    'query': '(all:graph) AND (all:unsupervised OR all:self-supervised OR all:representation learning OR all:networks)',
    'news': [
        {
            'arxiv_id': '2106.06682v2',
            'title': 'Solving PDEs on Unknown Manifolds with Machine Learning',
            'authors': 'Senwei Liang, Shixiao W. Jiang, John Harlim, Haizhao Yang',
            'published_at': '2021-06-12 03:55:15+00:00',
            'updated_at': '2022-06-10 17:48:38+00:00',
            'categories': ['math.NA', 'cs.LG', 'cs.NA'],
            'comments': '22 pages, 10 figures. Accepted at ICML 2022. Code available at https://github.com/joeloskarsson/graph-dgmrf',
            'abs': 'This paper proposes a mesh-free computational framework and machine learning theory for solving elliptic PDEs on unknown manifolds, identified with point clouds, based on diffusion maps (DM) and deep learning. The PDE solver is formulated as a supervised learning task to solve a least-squares regression problem that imposes an algebraic equation approximating a PDE (and boundary conditions if applicable). This algebraic equation involves a graph-Laplacian type matrix obtained via DM asymptotic expansion, which is a consistent estimator of second-order elliptic differential operators. The resulting numerical method is to solve a highly non-convex empirical risk minimization problem subjected to a solution from a hypothesis space of neural networks. In a well-posed elliptic PDE setting, when the hypothesis space consists of neural networks with either infinite width or depth, we show that the global minimizer of the empirical loss function is a consistent solution in the limit of large training data. When the hypothesis space is a two-layer neural network, we show that for a sufficiently large width, gradient descent can identify a global minimizer of the empirical loss function. Supporting numerical examples demonstrate the convergence of the solutions, ranging from simple manifolds with low and high co-dimensions, to rough surfaces with and without boundaries. We also show that the proposed NN solver can robustly generalize the PDE solution on new data points with generalization errors that are almost identical to the training errors, superseding a Nystrom-based interpolation method.',
            'doi': None,
            'urls': ['http://arxiv.org/abs/2106.06682v2', 'http://arxiv.org/pdf/2106.06682v2']
        },
        {
            'arxiv_id': '2106.06682v2',
            'title': 'RecoMed: A Knowledge-Aware Recommender System for Hypertension Medications',
            'authors': 'Maryam Sajde, Hamed Malek, Mehran Mohsenzadeh',
            'published_at': '2021-06-12 03:55:15+00:00',
            'updated_at': '2022-06-10 17:48:38+00:00',
            'categories': ['cs.IR', 'cs.NA'],
            'abs': """Background and Objective High medicine diversity has always been a
significant challenge for prescription, causing confusion or doubt in
physicians' decision-making process. This paper aims to develop a medicine
recommender system called RecoMed to aid the physician in the prescription
process of hypertension by providing information about what medications have
been prescribed by other doctors and figuring out what other medicines can be
recommended in addition to the one in question. Methods There are two steps to
the developed method: First, association rule mining algorithms are employed to
find medicine association rules. The second step entails graph mining and
clustering to present an enriched recommendation via ATC code, which itself
comprises several steps. First, the initial graph is constructed from
historical prescription data. Then, data pruning is performed in the second
step, after which the medicines with a high repetition rate are removed at the
discretion of a general medical practitioner. Next, the medicines are matched
to a well-known medicine classification system called the ATC code to provide
an enriched recommendation. And finally, the DBSCAN and Louvain algorithms
cluster medicines in the final step. Results A list of recommended medicines is
provided as the system's output, and physicians can choose one or more of the
medicines based on the patient's clinical symptoms. Only the medicines of class
2, related to high blood pressure medications, are used to assess the system's
performance. The results obtained from this system have been reviewed and
confirmed by an expert in this field.""",
            'doi': 'http://dx.doi.org/10.1016/j.imu.2022.100950',
            'urls': ['http://arxiv.org/abs/2106.06682v2', 'http://arxiv.org/pdf/2106.06682v2']
        }
    ]
}


@app.route("/")
def template_test():
    return render_template('template.html', **newsletter)


if __name__ == '__main__':
    app.run(debug=True)
