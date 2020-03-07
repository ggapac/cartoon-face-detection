path = "path_to_your_dir"
setwd(path)

if (!require("rjson")) install.packages("rjson")
if (!require("ggplot2")) install.packages("ggplot2")
library(rjson)
library(ggplot2)

results <- fromJSON(file = "./output/results.json")
# results <- fromJSON(file = "./output/results_2.json")

# Parameters
b <- 1000 # number of bootstrap repetitions
alpha <- 0.025 # we want (1 - 2 * alpha) * 100% confidence interval

bootstrap <- function(b, iou) {
  boot_samples <- replicate(b, sample(iou, replace = T))
  boot_distr <- apply(boot_samples, 2, mean)
}

boot_perc_interval <- function(boot_distr, alpha) {
  boot_distr <- sort(boot_distr)
  b <- length(boot_distr)
  
  cis <- c(boot_distr[round(alpha * b)], boot_distr[round((1 - alpha) * b)])
  return(cis)
}

df <- data.frame("Cartoon" = character(),
                 "IoU_mean" = double(),
                 "IoU_bootstrap_ci_lower" = double(),
                 "IoU_bootstrap_ci_upper" = double())

for(i in 1:length(results)) {
  boot_distr <- bootstrap(b, results[[i]])
  cis <- boot_perc_interval(boot_distr, alpha)
  df <- rbind(df, data.frame("Cartoon" = names(results)[i],
                             "IoU_mean" = mean(results[[i]]),
                             "IoU_bootstrap_ci_lower" = cis[1],
                             "IoU_bootstrap_ci_upper" = cis[2]))
}

p <- ggplot(df, aes(x = Cartoon, y = IoU_mean, label = Cartoon)) +
  geom_point() +
  geom_errorbar(aes(ymin = IoU_bootstrap_ci_lower, 
                    ymax = IoU_bootstrap_ci_upper),
                width = 0.3, size = 0.5) +
  geom_text(aes(label=Cartoon),hjust=0.5, vjust=-0.5) +
  theme_bw() + coord_flip() +
  labs(y = "Intersection over Union", x = NULL) +
  scale_x_discrete(breaks=NULL) +
  scale_y_continuous(limits = c(0, 0.6), breaks = seq(0, 0.6, length.out = 7))

ggsave("./output/plots/IoU_analysis.png", p,
       width = 6, height = 1.5, units = "in")


