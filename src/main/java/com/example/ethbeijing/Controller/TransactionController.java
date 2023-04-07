package com.example.ethbeijing.Controller;

import com.example.ethbeijing.common.R;

import com.example.ethbeijing.entity.Transaction;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Slf4j
@RestController
@RequestMapping("/data")
@CrossOrigin(origins = "*")
public class TransactionController {
    @Autowired
    private MongoTemplate mongoTemplate;
    @GetMapping("/{hash}")
    public R<Transaction> get(@PathVariable String hash){
        Transaction transaction = mongoTemplate.findOne(new Query(Criteria.where("tx_hash").is(hash.toString())),Transaction.class);
        return R.success(transaction);
    }
    @GetMapping("/page")
    public List<Transaction> findByPage(int pageIndex, int pageSize) {
        System.out.println(pageIndex+pageSize);
        if (pageIndex < 0) {
            pageIndex = 0;
        }
        if (pageSize < 10) {
            pageSize = 10;
        }
        Query query = new Query();
        Pageable pageable = PageRequest.of(pageIndex, pageSize);
        query.with(pageable);
        return mongoTemplate.find(query, Transaction.class);
    }
}
