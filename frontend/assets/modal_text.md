# Idea
Prettyfin visualizes the spending on the Swiss municipal level, aggregated over each canton.
It allows comparisons between cantons, departments and years.

# Visualizations 
Each tab visualizes the same data set but with different focus/axis.

## Bubble Graph
This is an interactive graph, based on the famous [Gapminder](https://www.gapminder.org/tools/#$chart-type=bubbles) 
visualization. 
* **Dropdowns 1 & 2** Let you select a spending category for the x & y axis.
* **Dropdown 3** Controls the size of the bubbles (similar to a z-axis). 
* **Normalized** Min-max-normalizes each canton to \[0,1\], i.e. 0 is the smallest value over all
 years in the specified axis, 1 the biggest value, separately calculated for each canton.
* **Correct for Inflation** Adjusts past amounts to have the real-world value of today.
* **Slider** The slider on the bottom adjusts the selected year and can be set to play the progress as an animation.

Different cantons can be deselected separately in the legend, double click to select only specific canton. 

## Line Graph 
This graph shows the spending over the years in the selected category. 
* **Dropdown** Lets you select a spending category for the x axis.
* **Normalized** This min-max-normalizes each canton to \[0,1\], i.e. 0 is the smallest value over all
 years in the specified axis, 1 the biggest value, separately calculated for each canton.
* **Correct for Inflation** Adjusts past amounts to have the real-world value of today.

## Map 
The map shows the values for each canton on a heat map in the specific year selected on the slider.

* **Dropdown** Lets you select a spending category heat map.
* **Correct for Inflation** Adjusts past amounts to have the real-world value of today.
* **Absolute** Min-max-normalizes all the values for all cantons over all years on \[0,1\], i.e. 0 is the smallest value 
in the whole category, 1 the largest.
* **Per Canton** Min-max-normalizes each canton to \[0,1\], i.e. 0 is the smallest value over all
 years in the specified axis, 1 the biggest value, separately calculated for each canton.
* **Per Year** Min-max-normalizes one category on one year to \[0,1\] over all cantons, i.e. 0 is the smallest value over 
all cantons in the specific year, 1 the largest.
* **Slider** The slider on the bottom adjusts the selected year and can be set to play the progress as an animation.

# Authors
The webpage and data visualization is done by [aiger](https://www.aiger.ch/). It is the first online visualization project and has the purpose of a POC.  

# Data Source
* Municipal spending data: [Eidgenössische Finanzverwaltung](https://www.efv.admin.ch/efv/de/home/themen/finanzstatistik/daten.html#-826253434)
* Population data: [Bundesamt für Statistik](https://www.bfs.admin.ch/bfs/de/home/statistiken/bevoelkerung/stand-entwicklung.assetdetail.9486033.html)
* Inflation rates: [Laenderdaten.info](https://www.laenderdaten.info/Europa/Schweiz/Inflationsraten.php)

# Technology
The complete application is developed as a [Dash](https://plot.ly/dash/) app, which brings Plotly visualizations to the web.