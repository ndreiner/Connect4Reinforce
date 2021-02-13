import numpy as np 



## Auxilary Function 
def convolve_2d(matrix,kernel):
    """
    Convolves a matrix with kernel on a 2d Basis

    Parameters
    ----------
    matrix : np.matrix with shape nxm
    kernel : np.matrix with shape smaller than matrix in both dims

    Returns
    -------
    res_matrix : np.matrix 

    """
    # Kernel dimensions
    ker_rows , ker_cols  = kernel.shape
  
    
    # matrix dimensions
    mat_rows , mat_cols = matrix.shape
    
    
    # compute max row and col indices to limit kernel calculation
    # and define result matrix
    max_row_index = mat_rows - ker_rows
    max_col_index = mat_cols - ker_cols
    
    res_matrix = np.zeros(shape = (max_row_index + 1 ,
                                   max_col_index + 1)
                          )# end np.zeros

    
    for cur_row in range(0,max_row_index+1, 1):
        for cur_col in range(0,max_col_index+1, 1):
            mat_slice = matrix[cur_row:(cur_row + ker_rows),
                               cur_col:(cur_col + ker_cols)]
 
            #kernel multiplikation (element wise)
            mat_slice = np.multiply(mat_slice,kernel)
            # write sum into result
            res_matrix[cur_row , cur_col] = np.sum(mat_slice)
    
    return res_matrix


## Main functions

class field():
    """
    PLaying Field functions for connect 4 
    """
    def __init__(self,FIELD_HEIGHT=6,FIELD_WIDTH=7):
        self.FIELD_HEIGHT = FIELD_HEIGHT
        self.FIELD_WIDTH  = FIELD_WIDTH
        self.field_matrix = np.zeros((self.FIELD_HEIGHT,self.FIELD_WIDTH))



    def show(self):
        """
         print the gamefield to the console
        """
        print(self.field_matrix)



    def get_matrix(self):
        """
        returns the matrix of the field
        Return: np.matrix
        """
        return self.field_matrix



    def drop(self, column_index, token):
        """
        drop a token at the specified column index
        """

        # Get rows with empty field values (value==0)
        dr_row_ind = np.flatnonzero(self.field_matrix[:,column_index])

        # there are already tokens in column, ergo Index list is not empty
        if dr_row_ind.size>0:
            # Drop at row before first nonzero value in col
            dr_row_ind = dr_row_ind[0]-1
        else : # if empty list
            dr_row_ind = self.FIELD_HEIGHT-1 
        

        if dr_row_ind<0 :
            raise IndexError("Error at CollumnIndex: "+ str(column_index)+
                            ". Column is already full!")

        self.field_matrix[dr_row_ind , column_index] = token
    
    def get_dropable_col_inds(self, as_bool = False):
        """
        returns  dropable indices if there are still playable rows
        """
        result = self.field_matrix[0,:]==0 # get bool matrix of first row
        result = np.array(result)
        result = np.squeeze(result)
        if not as_bool:
            # get indices of True Values
            result = np.where(result)
        return result
    
    def is_playable(self):
        """
        returns true if there is still one droppable column
        """
        result = self.get_dropable_col_inds(as_bool = True)
        return result.any()

    def check_win(self,n_connect_to_win, verbose = False):
        """
        check if a token has the right shape for a win
        output:
        np.nan = no winner
        0 = draw
        token value (either -1 or 1):
            Winning token
        """
        ## define kernels for wincheck
        # upper right to lower left
        kern_ur_ll = np.eye(n_connect_to_win)
        # upper lefto lower right
        kern_ul_lr = np.fliplr(kern_ur_ll)
        # horizontal 
        kern_h = np.ones((1,n_connect_to_win))
        # vertical
        kern_v = np.ones((n_connect_to_win,1))

        ## to convilutionss
        conv_ur_ll = convolve_2d(self.field_matrix,kern_ur_ll)
        conv_ul_lr = convolve_2d(self.field_matrix,kern_ul_lr)
        conv_h     = convolve_2d(self.field_matrix,kern_h)
        conv_v     = convolve_2d(self.field_matrix,kern_v) 
        
        res = map(lambda x: x.flatten(),[conv_ur_ll,conv_ul_lr,conv_h,conv_v])
        res = np.concatenate(list(res))
        res_min, res_max = np.min(res), np.max(res)
        result = np.nan
        if res_min <= (n_connect_to_win*-1):
            result = (-1)
        elif res_max >= n_connect_to_win:
            result = 1
        elif not self.is_playable():
            result = 0

        return result











class game():
    def __init__(self,field=field(),n_connect_to_win=4):
        self.field = field #Gamefield
        self.n_connect_to_win= n_connect_to_win #how many connected markers are needed for a win
        # check if winning is actually possible
        if (not any(self.field.field_matrix.shape)>n_connect_to_win):
            raise("Game is unwinnable as field is not large enough to hold lines needed to win")
    def exec_action(self,column_index,token):
        """
        executes a token drop on the desired index, immediately checks if the game is won
        Returns the win value
        """
        self.field.drop(column_index = column_index,
                        token = token)
        return(self.field.check_win(self.n_connect_to_win))
    def get_field(self):
        return(self.field.get_matrix())
    
    
class agent():
    def __init__(self,name,token,strategy,stochastic=False, tiebreak = 'first'):
        self.token = token
        self.name = name
        self.strategy = strategy
        self.stochastic = stochastic
        self.tiebreak = tiebreak
    
    def choose_action(self,cur_field, legal_indices):
        action_values = self.strategy(cur_field)
        chosen_ind = np.nan
        if not self.stochastic:
            if self.tiebreak == 'first':
                chosen_ind = np.argmax(action_values)
            elif self.tiebreak == 'random':
                action_values = np.where(action_values == np.max(action_values))
                chosen_ind = np.random.choice(action_values, size=1)
        else : # stochastic strategy chosen
            chosen_ind = np.random.choice(list(range(len(action_values))),
                                          size = 1,
                                          replace = False,
                                          p = action_values)
        
        return(chosen_ind)
    
    






###Testing functions
gamefield= field(3,3)
gamefield.show()
gamefield.drop(1, token = 1)
gamefield.drop(1, token = 1)
gamefield.drop(1, token = 1)
gamefield.drop(2, token = 1)

print(gamefield.check_win(n_connect_to_win = 3))

gamefield.show()
print(gamefield.get_dropable_col_inds())

array=np.array([[1,1,1,1],[0,0,0,0],[1,1,-1,-1],[-1,-1,-1,-1]])