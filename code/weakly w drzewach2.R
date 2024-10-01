library("igraph")

generuj <- function(ile){
  # random tree with root not leaf
  T <- make_tree(0)
  T <- add_vertices(T, ile, color = "white", sta = "", n00 = 0, n01 = 0, 
                    child = 0, n2 = 0, R = 0, sw = 0)
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
    V(T)[v]$n2 <- 0
    V(T)[v]$sta <- ""
    V(T)[v]$R <- 0
    V(T)[v]$sw <- 0
    V(T)[v]$child <- 0
    V(T)[v]$color = "white"
  }
  return(T)
}


phase0 <- function(T){
  for (v in vcount(T):1){
    father <- neighbors(T, v, "in")
    if (ego_size(T,1,v)-1 == 1){   # leaf
      V(T)[v]$sta <- "L"
      if (length(father))  {
        V(T)[father]$n00 <- V(T)[father]$n00 + 1
        V(T)[father]$child <- v
        if (V(T)[father]$sta == 'SW')  V(T)[father]$sta = 'S' 
        if (V(T)[father]$sta == '')    V(T)[father]$sta = 'SW'
      }
    }
    if (V(T)[v]$sta == 'SW' && length(father))  V(T)[father]$sw <- V(T)[father]$sw + 1
  }
  return(T)
}

phase1 <- function(T){
  for (v in vcount(T):1){
    father <- neighbors(T, v, "in")    # who is your father?
  
    if(V(T)[v]$sta != "L"){ # not leaf
      
      if(V(T)[v]$sw > 0 && V(T)[v]$sw + V(T)[v]$n00 + V(T)[v]$n01 > 1){ #col 4 - 5 
        V(T)[v]$R <- 2
        if (length(father)){
          V(T)[father]$n2 <- V(T)[father]$n2 + 1
           if(V(T)[v]$sta == "SW") V(T)[father]$sw <- V(T)[father]$sw - 1
        }   
        V(T)[v]$sta <- "ch"
      }
      
      if(V(T)[v]$sw == 0){ # not a father of a weak support
        
        if(V(T)[v]$sta == 'SW' && V(T)[v]$n00 + V(T)[v]$n01 > 1){
          V(T)[v]$sta <- 'S'
          if (length(father)) V(T)[father]$sw <- V(T)[father]$sw - 1
        }
        
        if(V(T)[v]$sta == 'S' || (V(T)[v]$sta == 'SW' && ego_size(T,1,v)-1 == 2)){ #1-2 col 
           V(T)[v]$R <- 2
           if (length(father))   V(T)[father]$n2 <- V(T)[father]$n2 + 1
        }
        
        if(V(T)[v]$sta == 'SW' && V(T)[v]$n2 > 0){   # 2 col
          V(T)[v]$R <- 0
          V(T)[V(T)[v]$child]$R <- 1
          if(length(father) && V(T)[v]$sta == "SW") V(T)[father]$sw <- V(T)[father]$sw - 1
        }
        
        if(!(V(T)[v]$sta %in% c("S", "SW"))){
          if (V(T)[v]$n00 > 0){
            V(T)[v]$R <- 2
            if (length(father))   V(T)[father]$n2 <- V(T)[father]$n2 + 1
          }
          else{
            if(V(T)[v]$n01 > 0) V(T)[v]$R <- 1
            }
          }
        
      }  # sw = 0
      if(V(T)[v]$R == 0 && V(T)[v]$n2 > 0 && length(father)) V(T)[father]$n01 <- V(T)[father]$n01 + 1
      if(V(T)[v]$R == 0 && V(T)[v]$n2 == 0 && length(father)) V(T)[father]$n00 <- V(T)[father]$n00 + 1
      cat("v = ", v, "sta = ", V(T)[v]$sta, "R = ",V(T)[v]$R, "n01= ",V(T)[v]$n01 ,"\n")
    } # not a leaf
  } # for
  if (V(T)[1]$n2 == 0 && V(T)[1]$R == 0)
    V(T)[1]$R <- 2 
  return(T)
}

phase2 <- function(T){
  for (v in vcount(T):1){
    father <- neighbors(T, v, "in")
    if(length(father)){
      if(V(T)[v]$sta == 'SW' && V(T)[father]$sta == 'ch'){
        V(T)[v]$R <- 0
        V(T)[V(T)[v]$child]$R <- 1
      }
    }
  }
  return(T)
}


T <- generuj(25)
#T <- kasuj(T)
T <- phase0(T)
T <- phase1(T)
T <- phase2(T)

for (v in V(T)){
  if (V(T)[v]$R == 2) V(T)[v]$color = "#EE767B"
  if (V(T)[v]$R == 1) V(T)[v]$color = "#599959"
  V(T)[v]$label = paste(v, V(T)[v]$sta)
}
tkplot(T, canvas.width = 500, canvas.height = 400, degree = 180, layout = layout_as_tree, edge.arrow.mode = "-")


for (v in V(T)) cat("v = ", v, "sta = ", V(T)[v]$sta, "R = ",V(T)[v]$R, " n01= ",V(T)[v]$n01 , " n00= ",V(T)[v]$n00 ," n2= ",V(T)[v]$n2 , "sw = ", V(T)[v]$sw, " \n")


#--------------------------- OLD -----------------------------------------

