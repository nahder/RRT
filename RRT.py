import matplotlib.pyplot as plt 
import numpy as np 
from numpy.linalg import norm

class RRT: 

    def __init__(self, q_init, q_goal, K, delta, D, num_circle_obstacles): 
        self.K = K 
        self.delta = delta
        self.D = D
        self.circle_obstacles = []
        self.q_goal = q_goal
        self.q_init = q_init    

        self.generate_circle_obstacles(num_circle_obstacles)

        if self.is_inside_obstacle(q_init):
            print("Initial point is inside an obstacle, regenerating...")
            self.q_init = self.generate_valid_pos()

        if self.is_inside_obstacle(q_goal):
            print("Goal point is inside an obstacle, regenerating...")
            self.q_goal = self.generate_valid_pos()

        self.G = self.create_RRT(K, delta)

    # checks if a point is inside any obstacle
    def is_inside_obstacle(self, point):
        for crc in self.circle_obstacles:
            center = np.array(crc[:2])
            radius = crc[2]
            if np.linalg.norm(np.array(point) - center) < radius:
                return True
        return False

    # generates a valid starting point outside of obstacles
    def generate_valid_pos(self):
        while True:
            point = (np.random.uniform(low=0, high=self.D[0]),
                     np.random.uniform(low=0, high=self.D[1]))
            if not self.is_inside_obstacle(point):
                return point
        
    def create_RRT(self, K, delta, tolerance=1.0):  
        G = {self.q_init: []}
        self.path = []
        goal_bias = 0.01

        for i in range(K):
            if np.random.rand() < goal_bias:
                q_rand = self.q_goal
            else:
                q_rand = self.generate_random_point()

            q_near = self.nearest_vertex(q_rand, G)
            q_new = self.new_configuration(q_near, q_rand, delta)

            if q_new not in G[q_near] and self.check_circle_collision(q_near, q_new):
                G[q_near].append(q_new)
                G[q_new] = []

                if np.linalg.norm(np.array(q_new) - np.array(self.q_goal)) <= tolerance:
                    G[q_new].append(self.q_goal)
                    G[self.q_goal] = []
                    self.path = self.find_path(G, self.q_goal)
                    if self.path:  
                        print("Path found, exiting...")
                        break
                    if i == K - 1:
                        print("No path found, exiting...")

        return G


    def find_path(self, G, goal):
        path = [goal]
        while path[-1] != self.q_init:
            current = path[-1]
            for parent in G:
                if current in G[parent]:
                    path.append(parent)
                    break
        return path[::-1]  

        
    #compute eucliean dist bw p1, p2
    def compute_distance(self,p1,p2): 
        p1 = np.array(p1) 
        p2 = np.array(p2) 
        return np.linalg.norm(p1-p2)

    def new_configuration(self, q_near, q_rand, delta):
        q_near = np.array(q_near)  # src
        q_rand = np.array(q_rand)  # dest

        v = q_rand - q_near
        dir_ = v / (np.linalg.norm(v) + 1e-6)  
        q_new = q_near + (delta * dir_)

        # check if path to q_new is collision-free
        if self.check_circle_collision(q_near, q_new):
            return tuple(q_new)
        else:
            # if there's a collision, find a collision-free point along the line
            for d in np.linspace(0, delta, num=100):
                q_test = q_near + (d * dir_)
                if not self.check_circle_collision(q_near, q_test):
                    return tuple(q_near + ((d - 0.1) * dir_))  # step back a little to ensure collision-free

            return q_near  # Return q_near if no collision-free point is found

    #find vertex in G closest to q_rand
    def nearest_vertex(self,q_rand,G): 
        min=np.inf
        min_dist_vertex=np.inf

        for vertex in G.keys(): #key: position, value: edges. append to the edges for nodes it is connected to
            dist = self.compute_distance(q_rand, vertex) 
            if dist < min: 
                min=dist 
                min_dist_vertex = vertex 
        
        return min_dist_vertex 

    #generate random point in domain D
    def generate_random_point(self): 
        return (np.random.uniform(low=0,high=self.D[0]),
                np.random.uniform(low=0,high=self.D[1]))
    
    
    #generate n circular obstacles
    def generate_circle_obstacles(self,n): 
        for _ in range(n):
            center = self.generate_random_point()
            r = np.random.uniform(low=2,high=self.D[0]/10)
            self.circle_obstacles.append([center[0],center[1],r])

    def check_circle_collision(self, q_near, q_new):
        q_near = np.array(q_near)
        q_new = np.array(q_new)
        line_vec = q_new - q_near

        line_vec_norm = np.linalg.norm(line_vec)
        if line_vec_norm < 1e-6:  
            return True  

        for crc in self.circle_obstacles:
            center = np.array(crc[:2])
            radius = crc[2]
            center_vec = center - q_near

            proj_length = np.dot(center_vec, line_vec) / line_vec_norm
            proj_vec = proj_length * (line_vec / line_vec_norm)

            # ensure the projection length is within the segment
            if proj_length < 0 or proj_length > line_vec_norm:
                closest_point = q_near if np.linalg.norm(center_vec) < np.linalg.norm(center - q_new) else q_new
            else:
                closest_point = q_near + proj_vec

            if np.linalg.norm(closest_point - center) < radius:
                return False  # collision detected

        return True  # no collision detected




        


        


         
    




        



