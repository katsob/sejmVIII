library(ape)
library(RColorBrewer)
library(rjson)

par(mar = par()$mar * c(.1,1,0,1))

dist_matrix = read.table('data/dist.txt', sep=',')
nm = read.csv('data/names_clubs.csv', stringsAsFactor=FALSE)
nms = nm[['index']]
kluby = nm[['club']]
colnames(dist_matrix) = nms

hc <- hclust(as.dist(dist_matrix), 'ward.D2')

colors <- c('#ffa700','#ab3d29','#00b22a','#00dad8','#fd0073','#E68310','#ebff4b','#A5AA99','#000000')
#colors <- c('#7F3C8D','#11A579','#3969AC','#F2B701','#E73F74','#E68310','#80BA5A','#A5AA99','#000000')
names(colors) <- unique(kluby)

# tips = unlist(sapply(nm, function(n) { if( n %in% names(dep)){ colors[dep[[n]]]}else{'#FFFFFF'}}))
tips = sapply(kluby, function(c) colors[c])
names(tips) = nms

pdf("RESULT.pdf", width = 15, height    = 15,pointsize = 4)
plot(as.phylo(hc), type='fan', cex=.8, lwd = 0.1, tip.color=tips, no.margin = F, label.offset = 0.05)
mtext('Posłowie VIII kadencji - podobieństwo głosowań', cex=7, line=-3)
mtext('na podstawie 800 ostatnich glosowań', cex=4, line=-10)
legend(x=-2.7, y=2.3, col = colors, legend = names(colors), pch=16, title='', cex=1.8, ncol=1, bty='n')
dev.off()


jpeg("RESULT.jpg", width = 1200, height    = 1200,pointsize = 1.8, res=450)
plot(as.phylo(hc), type='fan', cex=.8, lwd = 0.1, tip.color=tips, no.margin = F, label.offset = 0.05)
legend(x=-2.7, y=2.3, col = colors, legend = names(colors), pch=16, title='', cex=1.8, ncol=1, bty='n')
dev.off()
