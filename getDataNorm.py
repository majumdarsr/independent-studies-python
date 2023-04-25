def genDataNorm(datalist, FeatureSize, xmin, xmax):
    import numpy as np
    import random
    
    #shuffle data to reduce bias toward certain data points
    random.shuffle(datalist)
    output = []
    
    # generate random data points from a normal distribution
    gen_norm = lambda mu, std, n : np.random.normal(loc=mu, scale=std, size = n)
    
    # Choose features list containing either real data or generated data
    # The smallest value is -180 degree
    if len(datalist) >= 5: # No. of original datapoints 
        dataMean, dataStd = np.mean(datalist), np.std(datalist)
       
        # filter data to remove outliers, data sould be within (xmin, xmax) or mean +- 2*dataStd, whichever range is shorter
        output = [point for point in datalist \
                if (point >= max(xmin,(dataMean - 2*dataStd)) and point <= min(xmax,(dataMean + 2*dataStd)))]
        
        # if size of output is smaller than FeatureSize or not a multiple of FeatureSize
        extraVals = len(output) % FeatureSize
        if extraVals > 0:
            random_n = [val for val in gen_norm(dataMean, 2*dataStd, 1000) if (val >= xmin and val <= xmax)]
            output = output + random_n[:FeatureSize - extraVals]
        
    return output if output else datalist

print(genDataNorm(list(range(5)), 10, xmin=0, xmax=5))
print(genDataNorm(list(range(4)), 10, xmin=0, xmax=5))

#This gives 10 values within 0-4 although 0-13 are possible values, with 14 members in the input array
print(genDataNorm(list(range(14)), 10, xmin=0, xmax=5))
