library(igraph)
library(combinat)

generate_base_tree <- function(size) {
  # Tworzy pełny zbiór możliwych krawędzi dla kompletnego grafu
  edges <- combn(1:size, 2)
  return(t(edges))
}

is_tree <- function(edge_list, size) {
  # Sprawdza, czy graf jest drzewem: spójny, brak cykli, n-1 krawędzi
  g <- graph_from_edgelist(edge_list, directed = FALSE)
  return(is.connected(g) && is_forest(g) && gsize(g) == (size - 1))
}

visualize_unique_trees <- function(size) {
  base_edges <- generate_base_tree(size)
  edge_combinations <- combn(nrow(base_edges), size - 1, simplify = FALSE)

  unique_trees <- list()

  for (comb in edge_combinations) {
    edge_list <- base_edges[comb, , drop = FALSE]
    if (is_tree(edge_list, size)) {
      g <- graph_from_edgelist(as.matrix(edge_list), directed = FALSE)
      # Sprawdzamy, czy graf nie jest izomorficzny z już istniejącymi
      if (!any(sapply(unique_trees, function(tree) isomorphic(g, tree)))) {
        unique_trees <- append(unique_trees, list(g))
      }
    }
  }

  # Rysowanie unikalnych drzew
  num_trees <- length(unique_trees)
  n_cols <- 4
  n_rows <- ceiling(num_trees / n_cols)

  par(mfrow = c(n_rows, n_cols), mar = c(2, 2, 2, 2))

  for (i in seq_along(unique_trees)) {
    plot(unique_trees[[i]], layout = layout_as_tree(unique_trees[[i]], root = 1),
         main = paste("Tree", i), vertex.size = 30, vertex.color = "lightblue", vertex.label = NA)
  }
}

# Przykład użycia
visualize_unique_trees(6)
