library(sf)
library(tmap)
library(urbnmapr)
library(ggplot2)
library(dplyr)
library(tidyverse)

time_periods = c("first_wave","second_wave","vaccination","whole")
types = c("confirmed","deaths")#confirmed deaths

for ( time_period in time_periods){
  for(type in types){
    vars_to_plot = c("mean_temp","min_temp","max_temp","total_prec","rh")
    titles = c("Correlation with Mean Temperature","Correlation with Min Temperature",
               "Correlation with Max Temperature","Correlation with Total Precipitation",
               "Correlation with Relative Humidity")
    
    us_map <- get_urbn_map(map="counties",sf=TRUE)
    us_map$countyFIPS <- as.integer(us_map$county_fips)
    
    
    # map <- ggplot() +
    #   geom_sf(data = confirmed_first_wave_map,
    #           aes(fill="mean_temp"),lwd=0)
    plot_map <- function(map_data_met,var,title){
      map <- tm_shape(map_data_met)+
        tm_polygons(var,title=title,border.alpha = 0,legend.is.portrait=FALSE)+
        tm_layout(legend.stack = "horizontal",legend.outside = T,
                  legend.outside.position = "top")
      map
      
    }
    
    
    src_file = paste0("Meteorological Analysis/covid_",type,"-",time_period,"-spearman.csv")
    met_data <- read.csv(src_file)
    met_map <- merge(us_map,met_data,on="countyFIPS")
    
    
    maps = list()
    for(i in 1:5){
      maps[[i]] <- plot_map(map_data_met = met_map,var = vars_to_plot[i],title = titles[i])
    }
    
    map <- tmap_arrange(maps,ncol = 3)
    
    out_file = paste0("img/spearman_",type,"-",time_period,".tiff")
    tiff(out_file,res = 300,width=3000,height=2000)
    print(map)
    dev.off()
    
    
  }
  
}

