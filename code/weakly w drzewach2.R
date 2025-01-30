library("igraph")

generuj <- function(ile){
  # random tree with root not leaf
  T <- make_tree(0)
  T <- add_vertices(T, ile, color = "white", n00 = 0, n01 = 0, n1=0,
                    child = 0, n2 = 0, R = 0, sw = 0, ch = 0)
  T <- add.edges(T, c(1,2))
  T <- add.edges(T, c(1,3))
  for (i in c(4:ile)){
    T <- add.edges(T, c( sample(1:(i-1),1) ,i))
  }
  #T <- as.undirected(T, "each")
  return(T)
}

kasuj <- function(T){
  for (v in vcount(T):1) {
    V(T)[v]$n00 <- 0
    V(T)[v]$n01 <- 0
    V(T)[v]$n1 <- 0
    V(T)[v]$n2 <- 0
    V(T)[v]$ch <- 0
    V(T)[v]$R <- 0
    V(T)[v]$sw <- 0
    V(T)[v]$child <- 0
    V(T)[v]$color = "white"
  }
  return(T)
}


phase1 <- function(T){
  for (v in vcount(T):1){
    father <- neighbors(T, v, "in")    # who is your father?

    if (ego_size(T,1,v) - 1 - V(T)[v]$n1 == 1){   # leaf
      if (length(father))  {
        V(T)[father]$n00 <- V(T)[father]$n00 + 1
        V(T)[father]$child <- v
      }
    }  # leaf - rest in "else"
    else{
      if (V(T)[v]$n00 == 1 && length(father) && V(T)[v]$n01 == 0)  V(T)[father]$sw <- V(T)[father]$sw + 1

      if (V(T)[v]$sw > 0 && V(T)[v]$sw + V(T)[v]$n00 + V(T)[v]$n01 > 1){ #col 4 - 5
        V(T)[v]$R <- 2
        if (length(father)){
          V(T)[father]$n2 <- V(T)[father]$n2 + 1
          if (V(T)[v]$n00 == 1 && V(T)[v]$n01 == 0)  V(T)[father]$sw <- V(T)[father]$sw - 1
        }
        V(T)[v]$ch <- 1
      }

      if (V(T)[v]$sw == 0){

        if (V(T)[v]$n00 > 1 || (V(T)[v]$n00 == 1 && (V(T)[v]$n2 == 0 || V(T)[v]$n01 > 0))){
          V(T)[v]$R <- 2
          if (length(father))   V(T)[father]$n2 <- V(T)[father]$n2 + 1
        }

        else if (V(T)[v]$n00 == 1){   # 2 here n2>0 and n01 = 0
          V(T)[v]$R <- 0
          V(T)[V(T)[v]$child]$R <- 1
          if (length(father))   V(T)[father]$sw <- V(T)[father]$sw - 1
        }

        if (V(T)[v]$n00 == 0 && V(T)[v]$n01 > 0) {
          V(T)[v]$R <- 1
          if (length(father))   V(T)[father]$n1 <- V(T)[father]$n1 + 1
        }
      }  # sw == 0

      if(V(T)[v]$R == 0 && V(T)[v]$n2 > 0 && length(father)) V(T)[father]$n01 <- V(T)[father]$n01 + 1
      if(V(T)[v]$R == 0 && V(T)[v]$n2 == 0 && length(father)) V(T)[father]$n00 <- V(T)[father]$n00 + 1
    }

    #cat("v = ", v, "n00 = ", V(T)[v]$n00, "R = ",V(T)[v]$R, "n01= ",V(T)[v]$n01 ,"ch= ",V(T)[v]$ch ,"sw= ",V(T)[v]$sw, "\n")
  }  # for
  if (V(T)[1]$n2 == 0 && V(T)[1]$R == 0)
    V(T)[1]$R <- 2
  return(T)
}


phase2 <- function(T){
  for (v in vcount(T):1){
    father <- neighbors(T, v, "in")
    if(length(father)){
      if (V(T)[v]$n00 == 1 && V(T)[father]$ch && V(T)[v]$n01 == 0){
        V(T)[v]$R <- 0
        V(T)[V(T)[v]$child]$R <- 1
        V(T)[father]$n00 <- V(T)[father]$n00 + 1
      }
    }
  }
  return(T)
}

gtestree <- function(){
  # tree 10
  T <- make_tree(0)
  # T <- add_vertices(T, 13, color = "white", n1 = 0 , n00 = 0, n01 = 0,
  #                   child = 0, n2 = 0, R = 0, sw = 0, ch = 0)
  # T <- add.edges(T, c(1,2, 1,3, 1,4, 4,5, 5,6, 5,7, 7,8, 8,9, 9,10, 6,11, 11,12, 12,13))

# T <- add_vertices(T, 12, color = "white", n1 = 0, n00 = 0, n01 = 0,
#                     child = 0, n2 = 0, R = 0, sw = 0, ch = 0)
#   T <- add_edges(T, c(1,2, 1,3, 3,4, 4,5, 5,6, 2,7, 7,8, 7,9, 9,10, 9,11, 11,12))

  # T <- add_vertices(T, 31, color = "white", n1 = 0, n00 = 0, n01 = 0,
  #                   child = 0, n2 = 0, R = 0, sw = 0, ch = 0)
  # T <- add_edges(T, c(1,2, 1,3,
  #                     2,4, 2,5,
  #                     3,6, 3,7,
  #                     4,8, 4,9,
  #                     5,10, 5,11,
  #                     6,12, 6,13,
  #                     7,14, 7,15,
  #                     8,16, 8,17,
  #                     9,18, 9,19,
  #                     10,20, 10,21,
  #                     11,22, 11,23,
  #                     12,24, 12,25,
  #                     13,26, 13,27,
  #                     14,28, 14,29,
  #                     15,30, 15,31))
  T <- add_vertices(T, 10, color = "white", n1 = 0, n00 = 0, n01 = 0,
                    child = 0, n2 = 0, R = 0, sw = 0, ch = 0)
  T <- add_edges(T, c(1,2, 2,3, 3,4, 4,5, 5,6, 6,7, 7,8, 8,9, 8,10))
  return(T)
}

T <- gtestree()
# T <- generuj(9)
#T <- kasuj(T)
T <- phase1(T)
T <- phase2(T)

for (v in V(T)){
  if (V(T)[v]$R == 2) V(T)[v]$color = "#EE767B"
  if (V(T)[v]$R == 1) V(T)[v]$color = "#599959"
  V(T)[v]$label = paste(v)
}
tkplot(T, canvas.width = 1000, canvas.height = 500, degree = 180, layout = layout_as_tree, edge.arrow.mode = "-")


for (v in V(T)) cat("v = ", v, "ch = ", V(T)[v]$ch, "R = ",V(T)[v]$R,
                    " n01= ",V(T)[v]$n01 , " n00= ",V(T)[v]$n00 ,
                    " n2= ",V(T)[v]$n2 , "sw = ", V(T)[v]$sw,
                    " n1= ",V(T)[v]$n1 , " \n")



