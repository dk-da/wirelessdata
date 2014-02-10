source(file="/Users/mutech34/Downloads/entropy/R/mi.plugin.R")

myentropy <- function (ct) {
	-sum( (apply(ct,1,sum)/sum(ct)) * apply(ct,1,myentropy0))/log(ncol(ct))
}

myentropy0 <- function (pv) {
	p1 <- pv/sum(pv)
	p2 <- p1[p1 != 0]
	sum(p2 * log(p2) )
}

mypurity <- function (ct) {
	sum(apply(ct,1,max)) / sum(ct)
}

mynmi <- function (ct) {
	hc <- -myentropy0(apply(ct,1,sum))
	hc <- entropy(apply(ct,1,sum))
	ha <- -myentropy0(apply(ct,2,sum))
	ha <- entropy(apply(ct,2,sum))
	mymi <- ha - sum(-apply(ct,1,myentropy0))/log(ncol(ct))
	mymi <- mi.plugin(ct)
	mymi/max(ha,hc)
}

myfm <- function (ct) {
	fmmax <- 0
	ret <- 0
	imax <- length(ct[,1])
	jmax <- length(ct[1,])
	for (i in 1:imax ) {
		for (j in 1:jmax ) {
			r <- ct[i,j]/sum(ct[,j])
			p <- ct[i,j]/sum(ct[i,])
			if((r!=0) && (p!=0)){
				fm <- 2*r*p/(r+p)
			} else fm <- 0
			fmmax <- max(fm,fmmax)
		}
		ret <- ret + sum(ct[,j])*fmmax/sum(ct)
	}
	ret
}

kmeansAIC = function(fit){
	m = ncol(fit$centers)
	n = length(fit$cluster)
	k = nrow(fit$centers)
	D = fit$tot.withinss
	return(D + 2*m*k)
}



library("pracma")
kmpp <- function(X, k) {
        n <- nrow(X)
        C <- numeric(k)
        C[1] <- sample(1:n, 1)

        for (i in 2:k) {
            dm <- distmat(X, X[C, ])
            pr <- apply(dm, 1, min); pr[C] <- 0
            C[i] <- sample(1:n, 1, prob = pr)
        }

        kmeans(X, X[C, ])
}
