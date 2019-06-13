# relnCollFilt.py - Latent Feature-based Collaborative Filtering
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import random
import matplotlib.pyplot as plt
import urllib.request
from learnProblem import Learner
from utilities import Displayable

class CF_learner(Learner):
    def __init__(self,
                 rating_set,           # a Rating_set object
                 rating_subset = None, # subset of ratings to be used as training ratings
                 test_subset = None,   # subset of ratings to be used as test ratings
                 step_size = 0.01,     # gradient descent step size
                 reglz = 1.0, # the weight for the regularization terms
                 num_features = 10,    # number of hidden features
                 feature_range = 0.02   # features are initialized to be between
                                       # -feature_range and feature_range
                 ):
        self.rating_set = rating_set
        self.ratings = rating_subset or rating_set.training_ratings # whichever is not empty
        if test_subset is None:
            self.test_ratings = self.rating_set.test_ratings
        else:
            self.test_ratings = test_subset
        self.step_size = step_size
        self.reglz = reglz
        self.num_features = num_features
        self.num_ratings = len(self.ratings)
        self.ave_rating = (sum(rating for (user,item,rating,timestamp) in self.ratings)
                           /self.num_ratings)

        self.set_users_that_rated = {user for (user,item,rating,timestamp) in self.ratings}
        self.set_items_rated = {item for (user,item,rating,timestamp) in self.ratings}
        self.max_item_index = max(self.set_items_rated)+1
        self.max_user_index = max(self.set_users_that_rated)+1
        self.user_offset = [0]*(self.max_user_index)
        self.item_offset = [0]*(self.max_item_index)
        self.user_feat = [[random.uniform(-feature_range,feature_range)
                              for f in range(num_features)]
                             for i in range(self.max_user_index)]
        self.item_feat = [[random.uniform(-feature_range,feature_range)
                              for f in range(num_features)]
                             for i in range(self.max_item_index)]
        self.iter=0

    def stats(self):
        self.display(1,"ave sumsq error of mean for training=",
                  sum((self.ave_rating-rating)**2 for (user,item,rating,timestamp)
                      in self.ratings)/len(self.ratings))
        self.display(1,"ave sumsq error of mean for test=",
                  sum((self.ave_rating-rating)**2 for (user,item,rating,timestamp)
                      in self.test_ratings)/len(self.test_ratings))
        self.display(1,"error on training set",
                     self.evaluate(self.ratings))
        self.display(1,"error on test set",
                     self.evaluate(self.test_ratings))

    def prediction(self,user,item):
        """Returns prediction for this user on this item."""
        return (self.ave_rating
                          + self.user_offset[user]
                          + self.item_offset[item]
                          + sum([self.user_feat[user][f]*self.item_feat[item][f]
                                 for f in range(self.num_features)]))
      
    def learn(self, num_iter = 50):    
      """ do num_iter iterations of gradient descent."""
      for i in range(num_iter):
        self.iter += 1
        abs_error=0
        sumsq_error=0
        for (user,item,rating,timestamp) in random.sample(self.ratings,len(self.ratings)):
            error = self.prediction(user,item) - rating
            abs_error += abs(error)
            sumsq_error += error * error
            self.user_offset[user] -= self.step_size*error
            self.item_offset[item] -= self.step_size*error
            for f in range(self.num_features):
                self.user_feat[user][f] -= self.step_size*error*self.item_feat[item][f]
                self.item_feat[item][f] -= self.step_size*error*self.user_feat[user][f]
        for user in range(self.max_user_index):
             self.user_offset[user] -= self.step_size*self.reglz* self.user_offset[user]
             for f in range(self.num_features):
                 self.user_feat[user][f] -= self.step_size*self.reglz*self.user_feat[user][f]
        for item in range(self.max_item_index):
            self.item_offset[item] -= self.step_size*self.reglz*self.item_offset[item]
            for f in range(self.num_features):
                self.item_feat[item][f] -= self.step_size*self.reglz*self.item_feat[item][f]
        self.display(1,"Iteration",self.iter,
              "(Ave Abs,AveSumSq) training =",self.evaluate(self.ratings),
              "test =",self.evaluate(self.test_ratings))

    def evaluate(self,ratings):
        """returns (avergage_absolute_error, average_sum_squares_error) for ratings
        """
        abs_error = 0
        sumsq_error = 0
        if not ratings: return (0,0)
        for (user,item,rating,timestamp) in ratings:
            error = self.prediction(user,item) - rating
            abs_error += abs(error)
            sumsq_error += error * error
        return abs_error/len(ratings), sumsq_error/len(ratings)

    def plot_predictions(self,
                            examples = "test"):
        """
        examples is either "test" or "training" or the actual examples
        """
        if examples == "test":
            examples = self.test_ratings
        elif examples == "training":
            examples = self.ratings
        plt.ion()
        plt.xlabel("prediction")
        plt.ylabel("cumulative proportion")
        self.actuals = [[] for r in range(0,6)]
        for (user,item,rating,timestamp) in examples:
            self.actuals[rating].append(self.prediction(user,item))
        for rating in range(1,6):
            self.actuals[rating].sort()
            numrat=len(self.actuals[rating])
            yvals = [i/numrat for i in range(numrat)]
            plt.plot(self.actuals[rating], yvals, label="rating="+str(rating))
        plt.legend()
        plt.draw()
        
    def plot_feature(self,
                     f,               # feature
                     plot_all=False,  # true if all points should be plotted
                     num_points=200   # number of random points plotted if not all
                     ):
        """plot some of the user-movie ratings,
        if plot_all is true
        num_points is the number of points selected at random plotted.

        the plot has the users on the x-axis sorted by their value on feature f and
        with the items on the y-axis sorted by their value on feature f and 
        the ratings plotted at the corresponding x-y position.
        """
        plt.ion()
        plt.xlabel("users")
        plt.ylabel("items")
        user_vals = [self.user_feat[user][f]
                     for user in range(self.max_user_index+1)
                     if user in self.set_users_that_rated]
        item_vals = [self.item_feat[item][f]
                     for item in range(self.max_item_index+1)
                     if item in self.set_items_rated]
        plt.axis([min(user_vals)-0.02,
                  max(user_vals)+0.05,
                  min(item_vals)-0.02,
                  max(item_vals)+0.05])
        if plot_all:
            for (user,item,rating,timestamp) in self.ratings:
                plt.text(self.user_feat[user][f],
                         self.item_feat[item][f],
                         str(rating))
        else:
            for i in range(num_points):
                (user,item,rating,timestamp) = random.choice(self.ratings)
                plt.text(self.user_feat[user][f],
                         self.item_feat[item][f],
                         str(rating))
        plt.show()

class Rating_set(Displayable):
    def __init__(self,
                 date_split=892000000,
                 local_file=False,
                 url="http://files.grouplens.org/datasets/movielens/ml-100k/u.data",
                 file_name="u.data"):
        self.display(1,"reading...")
        if local_file:
            lines = open(file_name,'r')
        else:
            lines = (line.decode('utf-8') for line in urllib.request.urlopen(url))
        all_ratings = (tuple(int(e) for e in line.strip().split('\t'))
                        for line in lines)
        self.training_ratings = []
        self.training_stats = {1:0, 2:0, 3:0, 4:0 ,5:0}
        self.test_ratings = []
        self.test_stats = {1:0, 2:0, 3:0, 4:0 ,5:0}
        for rate in all_ratings:
            if rate[3] < date_split:   # rate[3] is timestamp
                self.training_ratings.append(rate)
                self.training_stats[rate[2]] += 1
            else:
                self.test_ratings.append(rate)
                self.test_stats[rate[2]] += 1
        self.display(1,"...read:", len(self.training_ratings),"training ratings and",
                len(self.test_ratings),"test ratings")
        self.tr_users = {user for (user,item,rating,timestamp) in self.training_ratings}
        self.test_users = {user for (user,item,rating,timestamp) in self.test_ratings}
        self.display(1,"users:",len(self.tr_users),"training,",len(self.test_users),"test,",
                     len(self.tr_users & self.test_users),"in common")
        tr_items = {item for (user,item,rating,timestamp) in self.training_ratings}
        test_items = {item for (user,item,rating,timestamp) in self.test_ratings}
        self.display(1,"items:",len(tr_items),"training,",len(test_items),"test,",
                     len(tr_items & test_items),"in common")
        self.display(1,"Rating statistics for training set: ",self.training_stats)
        self.display(1,"Rating statistics for test set: ",self.test_stats)

    def create_top_subset(self, num_items = 30, num_users = 30):
        """Returns a subset of the ratings by picking the most rated items,
        and then the users that have most ratings on these, and then all of the
        ratings that involve these users and items.
        """
        max_item_index = max(item for (user,item,rating,timestamp) in self.training_ratings)

        item_counts = [0]*(max_item_index+1)
        for (user,item,rating,timestamp) in self.training_ratings:
            item_counts[item] += 1

        items_sorted = sorted((item_counts[item],item) for item in range(max_item_index))
        top_items = items_sorted[-num_items:]
        set_top_items = set(item for (count, item) in top_items)

        max_user_index = max(user for (user,item,rating,timestamp) in self.training_ratings)
        user_counts = [0]*(max_user_index+1)
        for (user,item,rating,timestamp) in self.training_ratings:
            if item in set_top_items:
                user_counts[user] += 1

        users_sorted = sorted((user_counts[user],user)
                               for user in range(max_user_index))
        top_users = users_sorted[-num_users:]
        set_top_users = set(user for (count, user) in top_users)
        used_ratings = [ (user,item,rating,timestamp)
                         for (user,item,rating,timestamp) in self.training_ratings
                         if user in set_top_users and item in set_top_items]
        return used_ratings

movielens = Rating_set()
learner0 = CF_learner(movielens, num_features = 1)
#learner0.learn(50)
# learner0.plot_predictions(examples = "training")
# learner0.plot_predictions(examples = "test")
#learner0.plot_feature(0)
#movielens_subset = movielens.create_top_subset(num_items = 20, num_users = 20)
#learner1 = CF_learner(movielens, rating_subset=movielens_subset, test_subset=[], num_features=1)
#learner1.learn(1000)
#learner1.plot_feature(0,plot_all=True)

def sorted_r(lst):
    for i in range(len(lst)-1):
        if lst[i][3] > lst[i+1][3]:
            return False
    return True
        
def splits(rs):
    users = {u:0 for u in rs.tr_users.union(rs.test_users)}
    stats = [0]*200
    max_stats = 0
    nr = 0
    for (u,i,r,d) in rs.training_ratings + rs.test_ratings:
        users[u] += 1
        nr += 1
        if nr % 10000 == 0:
            stats = [0]*2000
            max_stats = 0
            for (u,n) in users.items():   # n is number of items u rated
                stats[n] += 1
                if n > max_stats:
                    max_stats = n
            print(nr,d,stats[:max_stats+1],max_stats)

splits(movielens)
                
