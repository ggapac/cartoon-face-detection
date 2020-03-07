path = "path_to_your_dir"
setwd(path)

if (!require("ggplot2")) install.packages("ggplot2")
library(ggplot2)


get_df <- function(cartoon_name, dat) {
  data.frame("cartoon" = cartoon_name,
             "type" = c("correct_ratio", "num_of_misdetected"),
             "vals" = c(sum(dat[, 2]) / sum(dat[, 3]),
                        sum(dat[, 4])))
}

frozen <- read.csv("./output/frozen/frozen_table.csv", header = T, sep = ";")[, 1:4]
simpsons <- read.csv("./output/simpsons/simpsons_table.csv", header = T, sep = ";")[, 1:4]
southpark <- read.csv("./output/southpark/southpark_table.csv", header = T, sep = ";")

df <- NULL
df <- rbind(df, get_df("frozen", frozen))
df <- rbind(df, get_df("simpsons", simpsons))
df <- rbind(df, get_df("southpark", southpark))


df$type <- as.factor(df$type)
levels(df$type) <- c("# correct detections / # all faces", "# misdetections")

p <- ggplot(df, aes(x = cartoon, fill = cartoon)) +
  geom_bar(aes(y = vals), stat="identity") +
  facet_wrap(~type, scale = "free") +
  scale_fill_manual(values = c("#B30000", "#2F1736", "#3374C0")) + 
  theme_bw() + labs(y = "count") +
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        axis.title.y=element_blank())

ggsave("./output/plots/count_analysis.png", p,
       width = 5.5, height = 3, units = "in")

