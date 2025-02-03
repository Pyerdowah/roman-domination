phase1 <- function(T){
  for (v in vcount(T):1){  # Iteracja po wszystkich wierzchołkach od ostatniego do pierwszego
    father <- neighbors(T, v, "in")  # Znalezienie ojca (rodzica) wierzchołka v

    # Sprawdzenie, czy wierzchołek v jest liściem
    if (ego_size(T, 1, v) - 1 - V(T)[v]$n1 == 1){  # Jeśli ma tylko jednego sąsiada (rodzica)
      if (length(father)) {  # Jeśli istnieje ojciec
        V(T)[father]$n00 <- V(T)[father]$n00 + 1  # Zwiększ licznik n00 ojca
        V(T)[father]$child <- v  # Zapisz, który wierzchołek jest dzieckiem
      }
    } else {  # Jeśli wierzchołek nie jest liściem (przejście do reszty przypadków)

      # Jeśli wierzchołek ma jedno dziecko z R = 0 i brak dzieci z R = 1
      if (V(T)[v]$n00 == 1 && length(father) && V(T)[v]$n01 == 0) {
        V(T)[father]$sw <- V(T)[father]$sw + 1  # Zwiększ licznik sw ojca
      }

      # Sprawdzenie, czy wierzchołek spełnia warunki na ustawienie R = 2
      if (V(T)[v]$sw > 0 && V(T)[v]$sw + V(T)[v]$n00 + V(T)[v]$n01 > 1) {
        V(T)[v]$R <- 2  # Ustaw R = 2 (dominujący węzeł)
        if (length(father)) {  # Jeśli istnieje ojciec
          V(T)[father]$n2 <- V(T)[father]$n2 + 1  # Zwiększ licznik n2 ojca
          if (V(T)[v]$n00 == 1 && V(T)[v]$n01 == 0) {
            V(T)[father]$sw <- V(T)[father]$sw - 1  # Zmniejsz sw ojca
          }
        }
        V(T)[v]$ch <- 1  # Ustaw ch = 1 (oznaczenie jako "ważne" dziecko)
      }

      # Jeśli licznik sw w wierzchołku jest równy 0
      if (V(T)[v]$sw == 0) {
        # Jeśli wierzchołek ma więcej niż jedno dziecko z R = 0
        if (V(T)[v]$n00 > 1 || (V(T)[v]$n00 == 1 && (V(T)[v]$n2 == 0 || V(T)[v]$n01 > 0))) {
          V(T)[v]$R <- 2  # Ustaw R = 2 (dominujący węzeł)
          if (length(father)) {
            V(T)[father]$n2 <- V(T)[father]$n2 + 1  # Zwiększ n2 ojca
          }
        } else if (V(T)[v]$n00 == 1) {  # Jeśli ma dokładnie jedno dziecko z R = 0
          V(T)[v]$R <- 0  # Ustaw R = 0 (neutralny węzeł)
          V(T)[V(T)[v]$child]$R <- 1  # Ustaw R = 1 dla dziecka
          if (length(father)) {
            V(T)[father]$sw <- V(T)[father]$sw - 1  # Zmniejsz sw ojca
          }
        }

        # Jeśli wierzchołek ma tylko dzieci z R = 1
        if (V(T)[v]$n00 == 0 && V(T)[v]$n01 > 0) {
          V(T)[v]$R <- 1  # Ustaw R = 1 (wspierający węzeł)
          if (length(father)) {
            V(T)[father]$n1 <- V(T)[father]$n1 + 1  # Zwiększ n1 ojca
          }
        }
      }

      # Aktualizacja liczników n00 i n01 dla ojca, jeśli wierzchołek ma R = 0
      if (V(T)[v]$R == 0 && V(T)[v]$n2 > 0 && length(father)) {
        V(T)[father]$n01 <- V(T)[father]$n01 + 1
      }
      if (V(T)[v]$R == 0 && V(T)[v]$n2 == 0 && length(father)) {
        V(T)[father]$n00 <- V(T)[father]$n00 + 1
      }
    }
  }

  # Ustawienie korzenia jako R = 2, jeśli nie jest zdominowany
  if (V(T)[1]$n2 == 0 && V(T)[1]$R == 0) {
    V(T)[1]$R <- 2
  }

  return(T)
}

phase2 <- function(T){
  for (v in vcount(T):1){  # Iteracja po wszystkich wierzchołkach od ostatniego do pierwszego
    father <- neighbors(T, v, "in")  # Znalezienie ojca wierzchołka v
    if (length(father)) {
      # Jeśli wierzchołek ma dokładnie jedno dziecko z R = 0, ojciec jest kluczowy, a brak dzieci z R = 1
      if (V(T)[v]$n00 == 1 && V(T)[father]$ch && V(T)[v]$n01 == 0) {
        V(T)[v]$R <- 0  # Ustaw R = 0 dla wierzchołka
        V(T)[V(T)[v]$child]$R <- 1  # Ustaw R = 1 dla dziecka
        V(T)[father]$n00 <- V(T)[father]$n00 + 1  # Zwiększ n00 ojca
      }
    }
  }

  return(T)
}
