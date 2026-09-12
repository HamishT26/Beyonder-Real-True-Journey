## 15 — One-shot final validation protocol

After the final commit is pushed and four-way equal, invoke final/canonical.txt once through an exclusive external latch. A success is never replayed. A failure remains zero success credit; any correction must be additive. The scope is owner-self and dependency-closed, not the complete repository suite or independent reproduction.
