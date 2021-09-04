setwd("C:/Users/meant/Downloads")
data=read.csv("abc.csv", header = TRUE) 

str(data)
summary(data)

#create a MIPS variable 
data$MIPS=(data$instructions/data$time)/1000000

library(tidyverse)
#changing scale from numerical to factor
data$scale=as.factor(data$scale)
#generate a scatter plot
data %>%
  ggplot(aes(x=MIPS, 
             y=power.energy.pkg., 
             color=Appname,shape=scale))+
  geom_point()+scale_shape_manual(values = c(15, 16,17))


ggplot(data, aes(x=MIPS, y=power.energy.pkg., color=scale)) + geom_point() + facet_grid(~Appname)

ggplot(data, aes(x=MIPS, y=power.energy.pkg., color=Appname)) + geom_point() + facet_grid(~CPU.Freq)


# bar plot 
ggplot(data=data, aes(x=Appname, y=time, fill=scale)) +
  geom_bar(stat="identity", position = "dodge")

dat_scaled <- as.data.frame(scale(data$time))
summary(dat_scaled)

#linear regression
model2=lm(data$power.energy.pkg.~., data=data)
summary(model2)
plot(model2$residuals)
abline(h=0,col='red')
#linear regression on all variable minus iteration and check model result
model1=lm(data$power.energy.pkg.~.-iteration, data=data)
summary(model1)
plot(model1$residuals)
abline(h=0,col='red')
#importance variable selection
library(leaps)
regfit.full=regsubsets(power.energy.pkg.~., data)
summary(regfit.full)
regfit.full=regsubsets(power.energy.pkg.~.,data=data,nvmax=20)
summary(regfit.full)
reg.summary=summary(regfit.full)
names(reg.summary)

data.frame(
  Adj.R2 = which.max(reg.summary$adjr2),
  CP = which.min(reg.summary$cp),
  BIC = which.min(reg.summary$bic)
)

par(mfrow=c(2,2))
plot(reg.summary$rss,xlab="Number of Variables",ylab="RSS",type="l")
plot(reg.summary$adjr2,xlab="Number of Variables",ylab="Adjusted RSq",type="l")

which.max(reg.summary$adjr2)  # identify the location of the maximum point of a vector
points(11,reg.summary$adjr2[11], col="red",cex=2,pch=20)
plot(reg.summary$cp,xlab="Number of Variables",ylab="Cp",type='l')
which.min(reg.summary$cp) # Cp is AIC
points(10,reg.summary$cp[10],col="red",cex=2,pch=20)
which.min(reg.summary$bic)
plot(reg.summary$bic,xlab="Number of Variables",ylab="BIC",type='l')
points(6,reg.summary$bic[6],col="red",cex=2,pch=20)

plot(regfit.full,scale="r2")
plot(regfit.full,scale="adjr2")
plot(regfit.full,scale="Cp")
plot(regfit.full,scale="bic")

#Variable Importance from tree base algorithem
library(caret)
set.seed(100)
rPartMod <- train(power.energy.pkg. ~ ., data=data, method="rpart")
rpartImp <- varImp(rPartMod)
print(rpartImp)
plot(rpartImp, top = 11, main='Variable Importance')

#correlation plot
library(corrplot)
data1 <- within(data, rm(Appname))
M<-cor(data1)
corrplot(M, method="number")

#outliner check and linear regression plot for each application with MIPS as oberseved value
library(neuralnet)

data$CPU.Freq_F=as.factor(data$CPU.Freq)
data_mine <- subset(data, Appname=="minebench")
out_m <- boxplot.stats(data_mine$power.energy.pkg.)$out
boxplot(data$power.energy.pkg.)
mtext(paste("Outliers: ", paste(out_m, collapse = ", ")))
data_mine %>%
  ggplot(aes(x=MIPS, 
             y=power.energy.pkg., 
             color=CPU.Freq_F))+
  geom_point()+
  geom_smooth(method="lm",se=T)+ggtitle("minebench")+theme(plot.title = element_text(hjust = 0.5))


data_fio <- subset(data, Appname=="fio")
out_f <- boxplot.stats(data_fio$power.energy.pkg.)$out
boxplot(data$power.energy.pkg.)
mtext(paste("Outliers: ", paste(out_f, collapse = ", ")))
data_fio %>%
  ggplot(aes(x=MIPS, 
             y=power.energy.pkg., 
             color=CPU.Freq_F))+
  geom_point()+
  geom_smooth(method="lm",se=F)+ggtitle("fio")+theme(plot.title = element_text(hjust = 0.5))


data_gapbs <- subset(data, Appname=="gapbs")
out_g <- boxplot.stats(data_gapbs$power.energy.pkg.)$out
boxplot(data$power.energy.pkg.)
mtext(paste("Outliers: ", paste(out_g, collapse = ", ")))
data_gapbs %>%
  ggplot(aes(x=MIPS, 
             y=power.energy.pkg., 
             color=CPU.Freq_F))+
  geom_point()+
  geom_smooth(method="lm")+ggtitle("gapbs")+theme(plot.title = element_text(hjust = 0.5))


data_nginx <- subset(data, Appname=="nginx")
out_n <- boxplot.stats(data_nginx$power.energy.pkg.)$out
boxplot(data$power.energy.pkg.)
mtext(paste("Outliers: ", paste(out_n, collapse = ", ")))
data_nginx %>%
  ggplot(aes(x=MIPS, 
             y=power.energy.pkg., 
             color=CPU.Freq_F))+
  geom_point()+
  geom_smooth(method="lm",se=F)+ggtitle("nginx")+theme(plot.title = element_text(hjust = 0.5))

data_schbench <- subset(data, Appname=="schbench")
out_s <- boxplot.stats(data_schbench$power.energy.pkg.)$out
boxplot(data$power.energy.pkg.)
mtext(paste("Outliers: ", paste(out_s, collapse = ", ")))
data_schbench %>%
  ggplot(aes(x=MIPS, 
             y=power.energy.pkg., 
             color=CPU.Freq_F))+
  geom_point()+
  geom_smooth(method="lm",se=T)+ggtitle("schbench")+theme(plot.title = element_text(hjust = 0.5))

