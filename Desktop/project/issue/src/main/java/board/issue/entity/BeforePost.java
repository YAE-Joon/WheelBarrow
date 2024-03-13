package board.issue.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter
@Setter
public class BeforePost {



    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long beforePostId;

    private String title;

    private String body;

    private Long user_id;

    private Long issue;

    private Long savedComment_id;


}
