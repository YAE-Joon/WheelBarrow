package board.issue.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.Setter;

@Getter
@Entity
@Setter
public class savedComments {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long savedComments_id;
    private String savedContent;
    private Long userId;

}
