data Unit a = Inch a | Cm a | Mm a | Pt a | Px a | Dxa a | Eme a deriving (Show)

class CollE s where
    empty  :: s
    
instance (Unit ) => CollE a where
    empty a = a
