library(sf)
library(tmap)
library(urbnmapr)
library(ggplot2)
library(dplyr)
library(tidyverse)

plot_map <- function(map_data_unauth,var,title){
  # map <- tm_shape(map_data_unauth)+
  #   tm_polygons(var,title=title,border.alpha = .2,legend.is.portrait=F)+
  #   tm_layout(legend.stack = "vertical",legend.outside = T,title.size = 16,legend.outside.position = "top")
    
  map <- tm_shape(map_data_unauth)+
    tm_fill(var,title = title,style = "equal",legend.is.portrait = F)+
    tm_borders(lwd=0.1)+
    tm_layout(legend.outside = T, legend.outside.position = "top",
              fontfamily = "serif")
  
  map
  
}


us_map <- get_urbn_map(map="counties",sf=TRUE)
us_map$countyFIPS <- as.integer(us_map$county_fips)

unauthorized_data <- read.csv("Unauthorized/county_unauthorized_processed.csv")
pop_data <- read.csv("Unauthorized/covid_county_population_usafacts.csv")
pop_data$countyFIPS <- as.integer(pop_data[,"ï..countyFIPS"])

unauthorized_data <- merge(unauthorized_data,pop_data,by="countyFIPS")
unauthorized_data <- unauthorized_data[,c("countyFIPS","Total.Unauthorized.Population","population")]
unauthorized_data$unauthorized_percentage <- unauthorized_data$Total.Unauthorized.Population/ unauthorized_data$population*100

map_data_unauth <- left_join(us_map,unauthorized_data,by="countyFIPS")
map_data_unauth$unauthorized_percentage[is.na(map_data_unauth$unauthorized_percentage)] <- 0

map_unauth <- plot_map(map_data_unauth,"unauthorized_percentage",
                       "Percentage of Illegal Immigrants(County Wise)")

tiff("img/unauth.tiff",height = 1500,width = 2000,res=300)
print(map_unauth)
dev.off()