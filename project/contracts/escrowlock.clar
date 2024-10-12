;; EscrowLock Smart Contract

;; Define constants
(define-constant contract-owner tx-sender)
(define-constant err-owner-only (err u100))
(define-constant err-not-found (err u101))
(define-constant err-invalid-state (err u102))

;; Define data vars
(define-data-var next-escrow-id uint u0)

;; Define map for storing escrow data
(define-map escrows
  uint
  {
    seller: principal,
    buyer: principal,
    amount: uint,
    state: (string-ascii 20)
  }
)

;; Create a new escrow
(define-public (create-escrow (buyer principal) (amount uint))
  (let
    (
      (escrow-id (var-get next-escrow-id))
    )
    (map-set escrows escrow-id
      {
        seller: tx-sender,
        buyer: buyer,
        amount: amount,
        state: "created"
      }
    )
    (var-set next-escrow-id (+ escrow-id u1))
    (ok escrow-id)
  )
)

;; Fund the escrow
(define-public (fund-escrow (escrow-id uint))
  (let
    (
      (escrow (unwrap! (map-get? escrows escrow-id) (err err-not-found)))
    )
    (asserts! (is-eq (get buyer escrow) tx-sender) (err err-owner-only))
    (asserts! (is-eq (get state escrow) "created") (err err-invalid-state))
    (try! (stx-transfer? (get amount escrow) tx-sender (as-contract tx-sender)))
    (map-set escrows escrow-id (merge escrow { state: "funded" }))
    (ok true)
  )
)

;; Release funds to the seller
(define-public (release-escrow (escrow-id uint))
  (let
    (
      (escrow (unwrap! (map-get? escrows escrow-id) (err err-not-found)))
    )
    (asserts! (is-eq (get buyer escrow) tx-sender) (err err-owner-only))
    (asserts! (is-eq (get state escrow) "funded") (err err-invalid-state))
    (try! (as-contract (stx-transfer? (get amount escrow) tx-sender (get seller escrow))))
    (map-set escrows escrow-id (merge escrow { state: "completed" }))
    (ok true)
  )
)

;; Get escrow details
(define-read-only (get-escrow (escrow-id uint))
  (map-get? escrows escrow-id)
)