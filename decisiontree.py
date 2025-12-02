import pandas as pd
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load JSON data
with open('youtube_data.json', "r", encoding="utf-8") as f:
    video_details = json.load(f)
    
video = []

for item in video_details:
    tags = item['snippet'].get('tags', [])
    number_of_tags = len(tags)
    view_count = item['statistics'].get('viewCount', 0)
    like_count = item['statistics'].get('likeCount', 0)
    category_id = item['snippet']['categoryId']
    comment_count = item['statistics'].get('commentCount', 0)
    
    video.append({
        'Views': view_count,
        'Comments': np.log(int(comment_count)+1),
        'Number of tags': np.log(number_of_tags+1),
        'category_id': category_id,
        'Likes': np.log(int(like_count)+1),
    })

df = pd.DataFrame(video)
column_order = ['Views','Comments','Number of tags','category_id','Likes']
df = df[column_order]
df = df.apply(pd.to_numeric)

X = df.drop('Likes', axis=1)
y = df['Likes']

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.2, random_state=23)

def best_split(X, y):
    best_feature = None
    best_split_value = None
    best_mse = float("inf")

    for feature in X.columns:
        values = X[feature].sort_values().unique()

        if len(values) < 2:
            continue

        split_points = [(a + b) / 2 for a, b in zip(values[:-1], values[1:])]

        for split in split_points:
            left_mask = X[feature] <= split
            right_mask = ~left_mask

            if left_mask.sum() == 0 or right_mask.sum() == 0:
                continue

            left_mean = y[left_mask].mean()
            right_mean = y[right_mask].mean()

            left_mse = ((y[left_mask] - left_mean) ** 2).mean()
            right_mse = ((y[right_mask] - right_mean) ** 2).mean()

            weighted_mse = (
                left_mask.sum() * left_mse +
                right_mask.sum() * right_mse
            ) / len(y)

            if weighted_mse < best_mse:
                best_mse = weighted_mse
                best_feature = feature
                best_split_value = split

    return best_feature, best_split_value, best_mse



## 3. Decision Tree Node Class

class TreeNode:
    def __init__(self, feature=None, split=None, left=None, right=None, value=None):
        self.feature = feature
        self.split = split
        self.left = left
        self.right = right
        self.value = value  # leaf node


## 4. Recursive Tree Builder

def build_tree(X, y, depth=0, max_depth=4, min_samples_split=8):

    # STOP CONDITIONS
    if len(y) < min_samples_split or depth == max_depth:
        return TreeNode(value=y.mean())

    feature, split, mse = best_split(X, y)

    if feature is None:
        return TreeNode(value=y.mean())

    left_mask = X[feature] <= split
    right_mask = ~left_mask

    left_child = build_tree(X[left_mask], y[left_mask], depth+1, max_depth)
    right_child = build_tree(X[right_mask], y[right_mask], depth+1, max_depth)

    return TreeNode(
        feature=feature,
        split=split,
        left=left_child,
        right=right_child
    )



##5. Function for Prediction

def predict_tree(node, sample):
    if node.value is not None:
        return node.value

    if sample[node.feature] <= node.split:
        return predict_tree(node.left, sample)
    else:
        return predict_tree(node.right, sample)


def predict(node, X):
    return np.array([predict_tree(node, X.iloc[i]) for i in range(len(X))])



## Training the tree

tree = build_tree(X_train, y_train, max_depth=4)
print("Decision Tree successfully trained.\n")


## Testing the model created

y_pred = predict(tree, X_test)
mse = np.mean((y_pred - y_test)**2)

print("Test MSE:", round(mse, 4))
print("\nSample Predictions:")
print(pd.DataFrame({'Actual Likes (log)': y_test.values[:3886],
                    'Predicted Likes (log)': y_pred[:3886]}))

residuals = y_test.values - y_pred

# Plot boxplot of residuals
plt.figure(figsize=(8,6))
plt.boxplot(residuals, vert=True, patch_artist=True)
plt.title("Box Plot of Prediction Residuals")
plt.ylabel("Residual (Actual - Predicted)")
plt.grid(True)
plt.show()