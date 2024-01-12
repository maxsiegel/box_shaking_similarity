library(tidyverse)

n_kids <- 10
n_trials <- 8

## success_probs <- c(.65, .7, .75)

success_fun <- function(disc, age) {
  1 / (1 + exp(-age / 3 * disc))
}
ages <- 3:6

disc_values <- seq(.5, 2, length.out = n_trials)

simulate_parameters <- function(n_kids, n_trials) {
  data <- tibble(kid = numeric(), age = numeric(), outcome = numeric(), disc = numeric(), prob_success = numeric())

  for (age in 1:3) {
    for (kid in 1:n_kids) {
      for (trial in 1:n_trials) {
        curr_disc <- disc_values[trial]
        outcome <- rbinom(1, 1, success_fun(curr_disc, age))

        data <- data %>% add_row(age = ages[age], outcome = outcome, kid = kid, disc = curr_disc, prob_success = success_fun(curr_disc, age))
      }
    }
  }

 p <- ggplot(data, aes(age, outcome)) +
    stat_summary(fun.data = mean_se, geom = "errorbar") +
    coord_cartesian(ylim = c(.5, 1))

  show(p)

  model <- aov(outcome ~ age, data = data)
  summary(model)
}

pval <- simulate_parameters(10, 8)
pval
