(define fibonacci
    (lambda (top)
        (begin
            (define fib
                (lambda (a b)
                    (begin
                        (define c (+ a b))
                        (display a)
                        (set! a b)
                        (set! b c)
                        (if (< a top)
                            (fib a b)))))
            (fib 0 1))))

(fibonacci 10)
