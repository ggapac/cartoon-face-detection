path = "path_to_your_dir"
setwd(path)

if (!require("ggplot2")) install.packages("ggplot2")
library(ggplot2)

frozen <- read.csv("./output/frozen/frozen_table.csv", header = T, sep = ";")[, 1:4]
frozen2 <- read.csv("./output/frozen_2/frozen_table_2.csv", header = T, sep = ";")

df <- data.frame("classifier" = c(rep("VJ face", 2), rep("VJ face + eyes", 2)),
                 "type" = c(rep(c("# correct detections", "# misdetections"), 2)),
                 "vals" = c(sum(frozen$num_of_correctly_detected),
                            sum(frozen$num_of_misdetected),
                            sum(frozen2$num_of_correctly_detected),
                            sum(frozen2$num_of_misdetected)))

p <- ggplot(df, aes(x = type, y = vals, fill = classifier)) +
  geom_bar(stat = "identity", position = "dodge") +
  scale_fill_manual(values = c("#B30000", "#2F1736")) + 
  geom_text(aes(label = vals), position = position_dodge(width = 0.9), vjust = -0.25) +
  theme_bw() +
  labs(y = "count")
  
ggsave("./output/plots/jv_combo_analysis.png", p,
       width = 5, height = 3.6, units = "in")
