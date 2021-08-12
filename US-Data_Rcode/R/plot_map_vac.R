library(sf)
library(tmap)
library(urbnmapr)
library(ggplot2)
library(dplyr)
library(tidyverse)

us_map <- get_urbn_map(map="states",sf=TRUE)
us_map$fips = as.integer(us_map$state_fips)

vac_data_confirmed <- read.csv("vaccination/covid_confirmed-vaccination-spearman.csv")
vac_data_cases <- cbind("fips"=as.integer(vac_data_confirmed$StateFIPS[3:nrow(vac_data_confirmed)]),
                        "Spearman" = as.numeric(vac_data_confirmed$people_vaccinated_per_hundred[3:nrow(vac_data_confirmed)]))
tmp <- read.csv("vaccination/covid_deaths-vaccination-spearman.csv")
vac_data_deaths <- cbind("fips"=as.integer(tmp$StateFIPS[3:nrow(tmp)]),
                         "Spearman" = as.numeric(tmp$people_vaccinated_per_hundred[3:nrow(tmp)]))

plot_map <- function(map_data_vac,var,title){
  map <- tm_shape(map_data_vac)+
    tm_polygons(var,title=title,border.alpha = 0,legend.is.portrait=T)+
    tm_layout(legend.stack = "vertical",legend.outside = T,legend.outside.position = "left")
  map
  
}

map_cases_vac <- merge(us_map,vac_data_cases,on="fips")
map_cases <- plot_map(map_cases_vac,"Spearman","(a) Spearman Correlations between\nDaily Number of Cases and\nNumber of People Vaccinated Daily")

map_deaths_vac <- merge(us_map,vac_data_deaths,on="fips")
map_deaths <- plot_map(map_deaths_vac,"Spearman","(b) Spearman Correlations between\nDaily Number of Deaths and\nNumber of People Vaccinated Daily")


map <- tmap_arrange(map_cases,map_deaths)

out_file = paste0("img/spearman_vac.tiff")
tiff(out_file,res = 300,width=3000,height=2000)
print(map)
dev.off()
# us_map$countyFS <- as.integer(us_map$county_fips)
