
PROBLEMS = {

    # 1. Find Maximum Element
    "q1": {
        "title": "Find Maximum Element",
        "entry_point": "find_max",

        "correct": [
            "def find_max(arr):\n    return max(arr)",
            "def find_max(arr):\n    best=arr[0]\n    for x in arr[1:]:\n        if x>best:\n            best=x\n    return best",
            "def find_max(arr):\n    best=arr[0]\n    i=1\n    while i<len(arr):\n        if arr[i]>best:\n            best=arr[i]\n        i+=1\n    return best"
        ],

        "wrong": [
            "def find_max(arr):\n    return min(arr)",
            "def find_max(arr):\n    return arr[0]",
            "def find_max(arr):\n    return sum(arr)"
        ],

        "tests": [
            {"args": [[1, 2, 3]], "expected": 3},
            {"args": [[-5, -1, -10]], "expected": -1},
            {"args": [[42]], "expected": 42},
            {"args": [[0, 0, 0]], "expected": 0},
            {"args": [[10, 5, 20, 15]], "expected": 20}
        ]
    },

    # 2. Check Prime Number
    "q2": {
        "title": "Check Prime Number",
        "entry_point": "is_prime",

        "correct": [
            "def is_prime(n):\n    if n<2:\n        return False\n    for i in range(2,int(n**0.5)+1):\n        if n%i==0:\n            return False\n    return True",

            "def is_prime(n):\n    if n<2:\n        return False\n    d=2\n    while d*d<=n:\n        if n%d==0:\n            return False\n        d+=1\n    return True",

            "def is_prime(n):\n    if n<2:\n        return False\n    for i in range(2,n):\n        if n%i==0:\n            return False\n    return True"
        ],

        "wrong": [
            "def is_prime(n):\n    return True",
            "def is_prime(n):\n    return n>1",
            "def is_prime(n):\n    if n<2:\n        return False\n    for i in range(2,int(n**0.5)):\n        if n%i==0:\n            return False\n    return True"
        ],

        "tests": [
            {"args": [0], "expected": False},
            {"args": [1], "expected": False},
            {"args": [2], "expected": True},
            {"args": [3], "expected": True},
            {"args": [4], "expected": False},
            {"args": [17], "expected": True},
            {"args": [25], "expected": False},
            {"args": [97], "expected": True}
        ]
    },

    # 3. Reverse a String
    "q3": {
        "title": "Reverse a String",
        "entry_point": "reverse_string",

        "correct": [
            "def reverse_string(s):\n    return s[::-1]",

            "def reverse_string(s):\n    out=''\n    for c in s:\n        out=c+out\n    return out",

            "def reverse_string(s):\n    out=[]\n    for c in s:\n        out.insert(0,c)\n    return ''.join(out)"
        ],

        "wrong": [
            "def reverse_string(s):\n    return s",
            "def reverse_string(s):\n    return s[1:]",
            "def reverse_string(s):\n    return s[:-1]"
        ],

        "tests": [
            {"args": ["hello"], "expected": "olleh"},
            {"args": ["a"], "expected": "a"},
            {"args": [""], "expected": ""},
            {"args": ["python"], "expected": "nohtyp"},
            {"args": ["12345"], "expected": "54321"}
        ]
    },

    # 4. Check Palindrome
    "q4": {
        "title": "Check Palindrome",
        "entry_point": "is_palindrome",

        "correct": [
            "def is_palindrome(s):\n    return s==s[::-1]",

            "def is_palindrome(s):\n    left=0\n    right=len(s)-1\n    while left<right:\n        if s[left]!=s[right]:\n            return False\n        left+=1\n        right-=1\n    return True",

            "def is_palindrome(s):\n    rev=''\n    for c in s:\n        rev=c+rev\n    return s==rev"
        ],

        "wrong": [
            "def is_palindrome(s):\n    return False",
            "def is_palindrome(s):\n    return s==s",
            "def is_palindrome(s):\n    return s[0]==s[-1] if s else True"
        ],

        "tests": [
            {"args": ["racecar"], "expected": True},
            {"args": ["hello"], "expected": False},
            {"args": ["a"], "expected": True},
            {"args": [""], "expected": True},
            {"args": ["abba"], "expected": True},
            {"args": ["abca"], "expected": False}
        ]
    },

    # 5. Factorial
    "q5": {
        "title": "Factorial",
        "entry_point": "factorial",

        "correct": [
            "def factorial(n):\n    if n==0:\n        return 1\n    return n*factorial(n-1)",

            "def factorial(n):\n    result=1\n    for x in range(2,n+1):\n        result*=x\n    return result",

            "def factorial(n):\n    result=1\n    x=1\n    while x<=n:\n        result*=x\n        x+=1\n    return result"
        ],

        "wrong": [
            "def factorial(n):\n    return n*2",
            "def factorial(n):\n    return n",
            "def factorial(n):\n    result=1\n    for x in range(1,n):\n        result*=x\n    return result"
        ],

        "tests": [
            {"args": [0], "expected": 1},
            {"args": [1], "expected": 1},
            {"args": [3], "expected": 6},
            {"args": [5], "expected": 120},
            {"args": [6], "expected": 720}
        ]
    },

    # 6. Sum of a List
    "q6": {
        "title": "Sum of a List",
        "entry_point": "sum_list",

        "correct": [
            "def sum_list(arr):\n    return sum(arr)",

            "def sum_list(arr):\n    total=0\n    for x in arr:\n        total+=x\n    return total",

            "def sum_list(arr):\n    total=0\n    i=0\n    while i<len(arr):\n        total+=arr[i]\n        i+=1\n    return total"
        ],

        "wrong": [
            "def sum_list(arr):\n    return arr[0] if arr else 0",
            "def sum_list(arr):\n    return len(arr)",
            "def sum_list(arr):\n    return sum(arr[:-1])"
        ],

        "tests": [
            {"args": [[1, 2, 3]], "expected": 6},
            {"args": [[10, 20]], "expected": 30},
            {"args": [[]], "expected": 0},
            {"args": [[-5, 5]], "expected": 0},
            {"args": [[1, 2, 3, 4, 5]], "expected": 15}
        ]
    },

    # 7. Count Frequency
    "q7": {
        "title": "Count Frequency",
        "entry_point": "count_frequency",

        "correct": [
            "def count_frequency(arr):\n    d={}\n    for x in arr:\n        d[x]=d.get(x,0)+1\n    return d",

            "def count_frequency(arr):\n    d={}\n    for x in arr:\n        if x in d:\n            d[x]+=1\n        else:\n            d[x]=1\n    return d",

            "def count_frequency(arr):\n    d={}\n    for x in set(arr):\n        d[x]=arr.count(x)\n    return d"
        ],

        "wrong": [
            "def count_frequency(arr):\n    return {}",
            "def count_frequency(arr):\n    return {x:1 for x in arr}",
            "def count_frequency(arr):\n    return dict.fromkeys(arr,1)"
        ],

        "tests": [
            {"args": [[1, 1, 2]], "expected": {1: 2, 2: 1}},
            {"args": [[]], "expected": {}},
            {"args": [["a", "a", "a"]], "expected": {"a": 3}},
            {"args": [[1, 2, 2, 3, 3, 3]], "expected": {1: 1, 2: 2, 3: 3}}
        ]
    },

    # 8. Find Duplicates
    "q8": {
        "title": "Find Duplicates",
        "entry_point": "find_duplicates",

        "correct": [
            "def find_duplicates(arr):\n    return sorted(set(x for x in arr if arr.count(x)>1))",

            "def find_duplicates(arr):\n    seen=set()\n    dup=set()\n    for x in arr:\n        if x in seen:\n            dup.add(x)\n        seen.add(x)\n    return sorted(dup)",

            "def find_duplicates(arr):\n    freq={}\n    for x in arr:\n        freq[x]=freq.get(x,0)+1\n    return sorted([x for x in freq if freq[x]>1])"
        ],

        "wrong": [
            "def find_duplicates(arr):\n    return arr",
            "def find_duplicates(arr):\n    return []",
            "def find_duplicates(arr):\n    return sorted([x for x in arr if arr.count(x)>1])"
        ],

        "tests": [
            {"args": [[1, 2, 2, 3]], "expected": [2]},
            {"args": [[1, 2, 3]], "expected": []},
            {"args": [[5, 5, 5]], "expected": [5]},
            {"args": [[1, 1, 2, 2, 3, 4, 4]], "expected": [1, 2, 4]},
            {"args": [[]], "expected": []}
        ]
    },

    # 9. Binary Search
    "q9": {
        "title": "Binary Search",
        "entry_point": "binary_search",

        "correct": [
            "def binary_search(arr,target):\n    l,r=0,len(arr)-1\n    while l<=r:\n        m=(l+r)//2\n        if arr[m]==target:\n            return m\n        if arr[m]<target:\n            l=m+1\n        else:\n            r=m-1\n    return -1",

            "def binary_search(arr,target):\n    left=0\n    right=len(arr)-1\n    while left<=right:\n        mid=left+(right-left)//2\n        if arr[mid]<target:\n            left=mid+1\n        elif arr[mid]>target:\n            right=mid-1\n        else:\n            return mid\n    return -1"
        ],

        "wrong": [
            "def binary_search(arr,target):\n    return 0",
            "def binary_search(arr,target):\n    return arr.index(target) if target in arr else 0",
            "def binary_search(arr,target):\n    l,r=0,len(arr)-1\n    while l<r:\n        m=(l+r)//2\n        if arr[m]==target:\n            return m\n        elif arr[m]<target:\n            l=m+1\n        else:\n            r=m-1\n    return -1"
        ],

        "tests": [
            {"args": [[1, 2, 3, 4, 5], 4], "expected": 3},
            {"args": [[1, 2], 5], "expected": -1},
            {"args": [[], 1], "expected": -1},
            {"args": [[2, 4, 6, 8, 10], 2], "expected": 0},
            {"args": [[2, 4, 6, 8, 10], 10], "expected": 4}
        ]
    },

    # 10. Balanced Parentheses
    "q10": {
        "title": "Balanced Parentheses",
        "entry_point": "is_balanced",

        "correct": [
            "def is_balanced(s):\n    stack=[]\n    for c in s:\n        if c=='(':\n            stack.append(c)\n        elif c==')':\n            if not stack:\n                return False\n            stack.pop()\n    return len(stack)==0",

            "def is_balanced(s):\n    count=0\n    for c in s:\n        if c=='(':\n            count+=1\n        elif c==')':\n            count-=1\n        if count<0:\n            return False\n    return count==0"
        ],

        "wrong": [
            "def is_balanced(s):\n    return True",
            "def is_balanced(s):\n    return len(s)%2==0",
            "def is_balanced(s):\n    return s.count('(')==s.count(')')"
        ],

        "tests": [
            {"args": ["()()"], "expected": True},
            {"args": ["(()"], "expected": False},
            {"args": [")("], "expected": False},
            {"args": [""], "expected": True},
            {"args": ["((()))"], "expected": True},
            {"args": ["(()())"], "expected": True},
            {"args": ["())("], "expected": False}
        ]
    }
}


